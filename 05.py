from utils import read_file

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


def get_value(pos, mode, lst):
    if mode == MODE_POS:
        return lst[lst[pos]]
    elif mode == MODE_IMM:
        return lst[pos]
    else:
        assert(False)


def set_value(pos, mode, lst, value):
    if mode == MODE_POS:
        lst[lst[pos]] = value
    elif mode == MODE_IMM:
        lst[pos] = value
    else:
        assert(False)


def run(ip, lst, inputs, outputs):
    opcode = "%05d" % lst[ip]
    a, b, c, op = int(opcode[0]), int(opcode[1]), int(opcode[2]), int(opcode[3:])

    if op == OP_HALT:
        return lst
    elif op == OP_ADD:
        v1 = get_value(ip + 1, c, lst)
        v2 = get_value(ip + 2, b, lst)
        set_value(ip + 3, a, lst, v1 + v2)
        ip += 4
    elif op == OP_MUL:
        v1 = get_value(ip + 1, c, lst)
        v2 = get_value(ip + 2, b, lst)
        set_value(ip + 3, a, lst, v1 * v2)
        ip += 4
    elif op == OP_INPUT:
        set_value(ip + 1, c, lst, inputs.pop(0))
        ip += 2
    elif op == OP_OUTPUT:
        outputs.append(get_value(ip + 1, c, lst))
        ip += 2
    elif op == OP_JIT:
        v1 = get_value(ip + 1, c, lst)
        if v1 != 0:
            ip = get_value(ip + 2, b, lst)
        else:
            ip += 3
    elif op == OP_JIF:
        v1 = get_value(ip + 1, c, lst)
        if v1 == 0:
            ip = get_value(ip + 2, b, lst)
        else:
            ip += 3
    elif op == OP_LT:
        v1 = get_value(ip + 1, c, lst)
        v2 = get_value(ip + 2, b, lst)
        if v1 < v2:
            set_value(ip + 3, a, lst, 1)
        else:
            set_value(ip + 3, a, lst, 0)
        ip += 4
    elif op == OP_EQ:
        v1 = get_value(ip + 1, c, lst)
        v2 = get_value(ip + 2, b, lst)
        if v1 == v2:
            set_value(ip + 3, a, lst, 1)
        else:
            set_value(ip + 3, a, lst, 0)
        ip += 4
    else:
        raise RuntimeError('invalid opcode: %d' % op)
    return run(ip, lst, inputs, outputs)


print("#--- part1 ---#")

assert(run(0, [1002, 4, 3, 4, 33], [], []) == [1002, 4, 3, 4, 99])
assert(run(0, [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [], [])
       == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])
assert(run(0, [1, 0, 0, 0, 99], [], []) == [2, 0, 0, 0, 99])
assert(run(0, [2, 3, 0, 3, 99], [], []) == [2, 3, 0, 6, 99])
assert(run(0, [2, 4, 4, 5, 99, 0], [], []) == [2, 4, 4, 5, 99, 9801])
assert(run(0, [1, 1, 1, 4, 99, 5, 6, 0, 99], [], []) == [30, 1, 1, 4, 2, 5, 6, 0, 99])

program = list(map(int, read_file('05.txt')[0].split(',')))
outputs = []
run(0, program, [1], outputs)
print(outputs[-1])


print("#--- part2 ---#")

# - Using position mode, consider whether the input is equal to 8; output 1 (if
#   it is) or 0 (if it is not).
outputs = []
run(0, [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [7], outputs)
assert(outputs[-1] == 0)
run(0, [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8], outputs)
assert(outputs[-1] == 1)
# - Using position mode, consider whether the input is less than 8; output 1 (if
#   it is) or 0 (if it is not).
run(0, [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [4], outputs)
assert(outputs[-1] == 1)
run(0, [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [9], outputs)
assert(outputs[-1] == 0)
# - Using immediate mode, consider whether the input is equal to 8; output 1 (if
#   it is) or 0 (if it is not).
run(0, [3, 3, 1108, -1, 8, 3, 4, 3, 99], [7], outputs)
assert(outputs[-1] == 0)
run(0, [3, 3, 1108, -1, 8, 3, 4, 3, 99], [8], outputs)
assert(outputs[-1] == 1)
# - Using immediate mode, consider whether the input is less than 8; output 1
#   (if it is) or 0 (if it is not).
run(0, [3, 3, 1107, -1, 8, 3, 4, 3, 99], [3], outputs)
assert(outputs[-1] == 1)
run(0, [3, 3, 1107, -1, 8, 3, 4, 3, 99], [10], outputs)
assert(outputs[-1] == 0)

program = list(map(int, read_file('05.txt')[0].split(',')))
outputs = []
run(0, program, [5], outputs)
print(outputs[-1])
