from utils import read_file
from intcode import Intcode, Task


def parse_map(output):
    map_ = {}
    x, y = 0, 0
    for char in task.outputs:
        if char == 10:
            y += 1
            x = 0
        else:
            map_[(x, y)] = char
            x += 1
    return map_


def get_max(map_):
    return max(x for x, _ in map_.keys()), max(y for _, y in map_.keys())


def print_map(map_):
    xmax, ymax = get_max(map_)
    for y in range(ymax + 1):
        for x in range(xmax + 1):
            print(chr(map_[(x, y)]), end='')
        print()


print("#--- part1 ---#")

program = list(map(int, read_file('17.txt')[0].split(',')))

vm = Intcode()
task = Task('part1', program, [76], ramsize=4096)
vm.run(task)

map_ = parse_map(task.outputs)
# print_map(map_)

xmax, ymax = get_max(map_)
intersections = []
for yy in range(1, ymax - 1):
    for xx in range(1, xmax - 1):
        if (map_[(xx, yy)] | map_[(xx - 1, yy)] | map_[(xx, yy - 1)] | map_[(xx + 1, yy)] | map_[(xx, yy + 1)]) == 35:
            intersections.append((xx * yy))
print(sum(intersections))


print("#--- part2 ---#")

# Sequence manually gathered from map:
#
# L,6,R,12,L,6,R,12,L,10,L,4,L,6,L,6,R,12,L,6,R,12,L,10,L,4,
# L,6,L,6,R,12,L,6,L,10,L,10,L,4,L,6,R,12,L,10,L,4,L,6,L,10,
# L,10,L,4,L,6,L,6,R,12,L,6,L,10,L,10,L,4,L,6

inputs = map(ord, 'A,B,A,B,A,C,B,C,A,C\x0a' + 'L,6,R,12,L,6\x0a' + 'R,12,L,10,L,4,L,6\x0a' + 'L,10,L,10,L,4,L,6\x0a' + 'n\x0a')

program = list(map(int, read_file('17.txt')[0].split(',')))
program[0] = 2

vm = Intcode()
task = Task('part1', program, list(inputs), ramsize=4096)
vm.run(task)
print(task.outputs.pop())
