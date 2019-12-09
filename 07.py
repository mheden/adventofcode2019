from utils import read_file
import itertools


class Intcode():

    OP_HALT = 99
    OP_ADD = 1
    OP_MUL = 2
    OP_INPUT = 3
    OP_OUTPUT = 4
    OP_JIT = 5
    OP_JIF = 6
    OP_LT = 7
    OP_EQ = 8

    MODE_POS = 0
    MODE_IMM = 1

    RES_OK = 0
    RES_DONE = 1
    RES_NEED_INPUT = -1

    def __init__(self, program, inputs):
        self._ip = 0
        self._inputs = []
        self._outputs = []
        self.add_inputs(inputs)
        self._program = program.copy()

    def _get_value(self, pos, mode):
        if mode == self.MODE_POS:
            return self._program[self._program[pos]]
        elif mode == self.MODE_IMM:
            return self._program[pos]
        else:
            assert(False)

    def _set_value(self, pos, mode, value):
        if mode == self.MODE_POS:
            self._program[self._program[pos]] = value
        elif mode == self.MODE_IMM:
            self._program[pos] = value
        else:
            assert(False)

    def add_inputs(self, inputs):
        # print("add_inputs(%s)" % inputs)
        for i in inputs:
            self._inputs.append(i)

    def pop_output(self):
        return self._outputs.pop(0)

    def step(self):
        opcode = "%05d" % self._program[self._ip]
        # print("step[%3d]: %s (inp:%s, out:%s)" % (self._ip, opcode, self._inputs, self._outputs))
        a, b, c, op = int(opcode[0]), int(opcode[1]), int(opcode[2]), int(opcode[3:])

        if op == self.OP_HALT:
            return self.RES_DONE
        elif op == self.OP_ADD:
            v1 = self._get_value(self._ip + 1, c)
            v2 = self._get_value(self._ip + 2, b)
            self._set_value(self._ip + 3, a, v1 + v2)
            self._ip += 4
        elif op == self.OP_MUL:
            v1 = self._get_value(self._ip + 1, c)
            v2 = self._get_value(self._ip + 2, b)
            self._set_value(self._ip + 3, a, v1 * v2)
            self._ip += 4
        elif op == self.OP_INPUT:
            if len(self._inputs) > 0:
                self._set_value(self._ip + 1, c, self._inputs.pop(0))
                self._ip += 2
            else:
                return self.RES_NEED_INPUT
        elif op == self.OP_OUTPUT:
            self._outputs.append(self._get_value(self._ip + 1, c))
            self._ip += 2
        elif op == self.OP_JIT:
            v1 = self._get_value(self._ip + 1, c)
            if v1 != 0:
                self._ip = self._get_value(self._ip + 2, b)
            else:
                self._ip += 3
        elif op == self.OP_JIF:
            v1 = self._get_value(self._ip + 1, c)
            if v1 == 0:
                self._ip = self._get_value(self._ip + 2, b)
            else:
                self._ip += 3
        elif op == self.OP_LT:
            v1 = self._get_value(self._ip + 1, c)
            v2 = self._get_value(self._ip + 2, b)
            if v1 < v2:
                self._set_value(self._ip + 3, a, 1)
            else:
                self._set_value(self._ip + 3, a, 0)
            self._ip += 4
        elif op == self.OP_EQ:
            v1 = self._get_value(self._ip + 1, c)
            v2 = self._get_value(self._ip + 2, b)
            if v1 == v2:
                self._set_value(self._ip + 3, a, 1)
            else:
                self._set_value(self._ip + 3, a, 0)
            self._ip += 4
        else:
            raise RuntimeError('invalid opcode: %d at IP=%d' % (op, self._ip))
        return self.RES_OK

    def run(self):
        res = self.step()
        while res == self.RES_OK:
            res = self.step()
        return res


def thrust(program, phase):
    a = Intcode(program, [phase[0], 0])
    a.run()
    b = Intcode(program, [phase[1], a.pop_output()])
    b.run()
    c = Intcode(program, [phase[2], b.pop_output()])
    c.run()
    d = Intcode(program, [phase[3], c.pop_output()])
    d.run()
    e = Intcode(program, [phase[4], d.pop_output()])
    e.run()
    return e.pop_output()


def thrust_fb(program, phase):
    vms = [Intcode(program, [phase[0]]),
           Intcode(program, [phase[1]]),
           Intcode(program, [phase[2]]),
           Intcode(program, [phase[3]]),
           Intcode(program, [phase[4]])]

    inp = 0
    while True:
        status = set()
        for vm in vms:
            vm.add_inputs([inp])
            status.add(vm.run())
            inp = vm.pop_output()
        if list(status) == [Intcode.RES_DONE]:
            return inp


print("#--- part1 ---#")

assert(thrust([3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15,
               15, 4, 15, 99, 0, 0], [4, 3, 2, 1, 0]) == 43210)
assert(thrust([3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23, 101,
               5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0], [0, 1, 2, 3, 4]) == 54321)
assert(thrust([3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
               1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0], [1, 0, 4, 3, 2]) == 65210)

program = list(map(int, read_file('07.txt')[0].split(',')))
print(max(thrust(program, phase) for phase in itertools.permutations(range(0, 5))))


print("#--- part2 ---#")

assert(thrust_fb([3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26, 27,
                  4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5], [9, 8, 7, 6, 5]) == 139629729)
assert(thrust_fb([3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
                  -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
                  53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10], [9, 7, 8, 5, 6]) == 18216)

program = list(map(int, read_file('07.txt')[0].split(',')))
print(max(thrust_fb(program, phase) for phase in itertools.permutations(range(5, 10))))
