class Task():

    def __init__(self, name, program, inputs=[], ramsize=None, verbose=False):
        self.name = name
        self.inputs = []
        self.outputs = []
        self.verbose = verbose
        self.regs = {'ip': 0, 'bp': 0}
        if ramsize is None:
            self.mem = program.copy()
        else:
            self.mem = [0 for _ in range(ramsize)]
            for i in range(len(program)):
                self.mem[i] = program[i]
        if len(inputs) > 0:
            self.write(inputs)

    def __repr__(self):
        return 'task(%s, ip=%d bp=%d in=%s out=%s)' % (self.name,
                                                       self.regs['ip'],
                                                       self.regs['bp'],
                                                       self.inputs,
                                                       self.outputs)

    def _log(self, msg):
        if self.verbose:
            print("[task %s] %s" % (self.name, msg))

    def write(self, inputs):
        if isinstance(inputs, list):
            for i in inputs:
                self.write(i)
        else:
            self.inputs.append(inputs)

    def read(self):
        data = []
        while True:
            try:
                data.append(self.outputs.pop(0))
            except IndexError:
                return data


class Intcode():

    OP_ADD = 1
    OP_MUL = 2
    OP_INPUT = 3
    OP_OUTPUT = 4
    OP_JEQ = 5
    OP_JNE = 6
    OP_LT = 7
    OP_EQ = 8
    OP_ADDBP = 9
    OP_HALT = 99

    MODE_POS = 0
    MODE_IMM = 1
    MODE_REL = 2

    STATE_NONE = 0
    STATE_READY = 1 << 0
    STATE_WAIT = 1 << 1
    STATE_DONE = 1 << 2

    state_names = {
        STATE_NONE: 'NONE',
        STATE_READY: 'READY',
        STATE_WAIT: 'WAIT',
        STATE_DONE: 'DONE',
    }

    def __init__(self, verbose=False, trace=False):
        self.tasks = []
        self.channels = {}
        self.states = {}
        self.trace = trace
        self.verbose = verbose
        self._log("starting machine...")

    def _log(self, msg):
        if self.verbose:
            print("[intcode] %s" % msg)

    def _set_state(self, task, state):
        if state != self.states[task]:
            self._log('%s: %s -> %s' % (task,
                                        self.state_names[self.states[task]],
                                        self.state_names[state]))
            self.states[task] = state

    def print_channels(self):
        print("%-40s  %s" % ('from', 'to'))
        for from_, to_ in self.channels.items():
            print("%-40s  %s" % (from_.name, [t.name for t in to_]))

    def print_tasks(self):
        print("%-40s  %s" % ('task', 'state'))
        for task in self.tasks:
            print("%-40s  %s" % (task, self.state_names[self.states[task]]))

    def connect(self, from_, to_):
        self._log("connect %s -> %s" % (from_.name, to_.name))
        if from_ not in self.channels:
            self.channels[from_] = []
        self.channels[from_].append(to_)

    def load(self, tasks):
        if not isinstance(tasks, list):
            tasks = [tasks]
        for task in tasks:
            self.tasks.append(task)
            self.states[task] = Intcode.STATE_NONE
            self._set_state(task, Intcode.STATE_READY)

    def send(self, task, values):
        task.write(values)
        if self.states[task] != Intcode.STATE_DONE:
            self._set_state(task, Intcode.STATE_READY)

    def run(self, tasks=[]):
        self.load(tasks)
        if len(self.tasks) == 0:
            raise RuntimeError("No tasks")

        state = Intcode.STATE_NONE
        while state != Intcode.STATE_DONE and state != Intcode.STATE_WAIT:
            state = Intcode.STATE_NONE
            for task in self.tasks:
                if self.states[task] != Intcode.STATE_READY:
                    continue
                self._task_run(task)
                if task in self.channels:
                    value = task.read()
                    for receiver in self.channels[task]:
                        self._log("send %s from %s to %s" % (value, task.name, receiver.name))
                        self.send(receiver, value)
            for s in self.states.values():
                state |= s
        return state

    def _pos(self, task, modes):
        indexes = []
        offset = 1
        for mode in modes:
            if mode == self.MODE_POS:
                indexes.append(task.mem[task.regs['ip'] + offset])
            elif mode == self.MODE_IMM:
                indexes.append(task.regs['ip'] + offset)
            elif mode == self.MODE_REL:
                indexes.append(task.regs['bp'] + task.mem[task.regs['ip'] + offset])
            offset += 1
        return indexes

    def _trace(self, msg):
        if self.trace:
            self._log(msg)

    def _step(self, task):
        opcode = "%05d" % task.mem[task.regs['ip']]
        m2, m1, m0, op = int(opcode[0]), int(opcode[1]), int(opcode[2]), int(opcode[3:])

        # print(task.regs['ip'], opcode, task.mem[task.regs['ip']:task.regs['ip']+6])

        if op == Intcode.OP_HALT:
            self._trace('%4d:\tHALT' % (task.regs['ip']))
            return Intcode.STATE_DONE

        elif op == Intcode.OP_ADD:
            p = self._pos(task, [m0, m1, m2])
            self._trace('%4d:\tADD\t[%d],\t[%d],\t[%d]' % (task.regs['ip'], *p))
            task.mem[p[2]] = task.mem[p[1]] + task.mem[p[0]]
            task.regs['ip'] += 4

        elif op == Intcode.OP_MUL:
            p = self._pos(task, [m0, m1, m2])
            self._trace('%4d:\tMUL\t[%d],\t[%d],\t[%d]' % (task.regs['ip'], *p))
            task.mem[p[2]] = task.mem[p[1]] * task.mem[p[0]]
            task.regs['ip'] += 4

        elif op == Intcode.OP_INPUT:
            if len(task.inputs) > 0:
                p = self._pos(task, [m0])
                self._trace('%4d:\tIN\t[%d]' % (task.regs['ip'], *p))
                task.mem[p[0]] = task.inputs.pop(0)
                task.regs['ip'] += 2
            else:
                self._trace('%4d:\tIN (buffer empty)' % (task.regs['ip']))
                return Intcode.STATE_WAIT

        elif op == Intcode.OP_OUTPUT:
            p = self._pos(task, [m0])
            self._trace('%4d:\tOUT\t[%d]' % (task.regs['ip'], *p))
            task.outputs.append(task.mem[p[0]])
            task.regs['ip'] += 2

        elif op == Intcode.OP_JEQ:
            p = self._pos(task, [m0, m1])
            self._trace('%4d:\tJEQ\t[%d],\t[%d]' % (task.regs['ip'], *p))
            if task.mem[p[0]] == 0:
                task.regs['ip'] += 3
            else:
                task.regs['ip'] = task.mem[p[1]]

        elif op == Intcode.OP_JNE:
            p = self._pos(task, [m0, m1])
            self._trace('%4d:\tJNE\t[%d],\t[%d]' % (task.regs['ip'], *p))
            if task.mem[p[0]] == 0:
                task.regs['ip'] = task.mem[p[1]]
            else:
                task.regs['ip'] += 3

        elif op == Intcode.OP_LT:
            p = self._pos(task, [m0, m1, m2])
            self._trace('%4d:\tLT\t[%d],\t[%d],\t[%d]' % (task.regs['ip'], *p))
            task.mem[p[2]] = 1 if task.mem[p[0]] < task.mem[p[1]] else 0
            task.regs['ip'] += 4

        elif op == Intcode.OP_EQ:
            p = self._pos(task, [m0, m1, m2])
            self._trace('%4d:\tEQ\t[%d],\t[%d],\t[%d]' % (task.regs['ip'], *p))
            task.mem[p[2]] = 1 if task.mem[p[0]] == task.mem[p[1]] else 0
            task.regs['ip'] += 4

        elif op == Intcode.OP_ADDBP:
            p = self._pos(task, [m0])
            self._trace('%4d:\tADDBP\t[%d]' % (task.regs['ip'], *p))
            task.regs['bp'] += task.mem[p[0]]
            task.regs['ip'] += 2

        else:
            raise RuntimeError('invalid opcode: %d at IP=%d' % (op, task.regs['ip']))

        return Intcode.STATE_READY

    def _task_run(self, task):
        self._log("start %s" % task)
        while self.states[task] == Intcode.STATE_READY:
            self._set_state(task, self._step(task))
        return self.states[task]


def test_day02():
    vm = Intcode()

    tasks = [
        Task('a', [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50]),
        Task('b', [1, 0, 0, 0, 99]),
        Task('c', [2, 3, 0, 3, 99]),
        Task('d', [2, 4, 4, 5, 99, 0]),
        Task('e', [1, 1, 1, 4, 99, 5, 6, 0, 99]),
    ]
    expected = [
        [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50],
        [2, 0, 0, 0, 99],
        [2, 3, 0, 6, 99],
        [2, 4, 4, 5, 99, 9801],
        [30, 1, 1, 4, 2, 5, 6, 0, 99]
    ]

    vm.run(tasks)
    for i, expect in enumerate(expected):
        assert(vm.tasks[i].mem == expect)


def test_day05():
    vm = Intcode()

    vm.run(Task('a', [1002, 4, 3, 4, 33]))
    assert(vm.tasks[0].mem == [1002, 4, 3, 4, 99])

    vm = Intcode()
    tasks = [
        Task('a', [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [7]),
        Task('b', [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8]),
        Task('c', [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [4]),
        Task('d', [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [9]),
        Task('e', [3, 3, 1108, -1, 8, 3, 4, 3, 99], [7]),
        Task('f', [3, 3, 1108, -1, 8, 3, 4, 3, 99], [8]),
        Task('g', [3, 3, 1107, -1, 8, 3, 4, 3, 99], [3]),
        Task('h', [3, 3, 1107, -1, 8, 3, 4, 3, 99], [10]),
    ]
    expected = [
        0, 1, 1, 0, 0, 1, 1, 0
    ]

    vm.run(tasks)
    for i, expect in enumerate(expected):
        assert(vm.tasks[i].outputs[-1] == expect)


def test_day07():

    def thrust(program, phase):
        vm = Intcode()

        a = Task('AmpA', program, [phase[0], 0])
        b = Task('AmpB', program, [phase[1]])
        c = Task('AmpC', program, [phase[2]])
        d = Task('AmpD', program, [phase[3]])
        e = Task('AmpE', program, [phase[4]])

        vm.load([a, b, c, d, e])
        vm.connect(a, b)
        vm.connect(b, c)
        vm.connect(c, d)
        vm.connect(d, e)

        vm.run()
        return e.outputs[0]

    assert(thrust([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15,
                   15, 4, 15, 99, 0, 0], [4, 3, 2, 1, 0]) == 43210)
    assert(thrust([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101,
                   5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0, 1, 2, 3, 4]) == 54321)
    assert(thrust([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
                   1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], [1, 0, 4, 3, 2]) == 65210)

    def thrust_feedback(program, phase):
        vm = Intcode()

        a = Task('AmpA', program, [phase[0], 0])
        b = Task('AmpB', program, [phase[1]])
        c = Task('AmpC', program, [phase[2]])
        d = Task('AmpD', program, [phase[3]])
        e = Task('AmpE', program, [phase[4]])

        vm.load([a, b, c, d, e])
        vm.connect(a, b)
        vm.connect(b, c)
        vm.connect(c, d)
        vm.connect(d, e)
        vm.connect(e, a)

        vm.run()
        return a.inputs[0]

    assert(thrust_feedback([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27,
                            4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5], [9, 8, 7, 6, 5]) == 139629729)
    assert(thrust_feedback([3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
                            -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
                            53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10], [9, 7, 8, 5, 6]) == 18216)


def test_day09():
    vm = Intcode()
    program = [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99]
    vm.run(Task('a', program, ramsize=4096))
    assert(program == vm.tasks[0].outputs)

    vm = Intcode()
    vm.run(Task('a', [1102, 34915192, 34915192, 7, 4, 7, 99, 0]))
    assert(len(str(vm.tasks[0].outputs[0])) == 16)

    vm = Intcode()
    vm.run(Task('a', [104, 1125899906842624, 99]))
    assert(vm.tasks[0].outputs[0] == 1125899906842624)


if __name__ == "__main__":
    test_day02()
    test_day05()
    test_day07()
    test_day09()
