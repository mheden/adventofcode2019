from utils import read_file
from intcode import Intcode, Task


def parse_outputs(outputs, points, ballx, paddlex):
    while len(outputs) > 0:
        x = vm.tasks[0].outputs.pop(0)
        y = vm.tasks[0].outputs.pop(0)
        tile = vm.tasks[0].outputs.pop(0)
        if x == -1 and y == 0:
            points = tile
        if tile == 4:
            ballx = x
        if tile == 3:
            paddlex = x
    return points, ballx, paddlex


print("#--- part1 ---#")

program = list(map(int, read_file('13.txt')[0].split(',')))
vm = Intcode()
vm.run(Task('part1', program, [], ramsize=4096))
print(vm.tasks[0].outputs[2::3].count(2))


print("#--- part2 ---#")

program = list(map(int, read_file('13.txt')[0].split(',')))
vm = Intcode()
vm.load(Task('part2', program, [], ramsize=4096))
vm.tasks[0].mem[0] = 2

points, ballx, paddlex = 0, 0, 0
state = vm.run()
while state != Intcode.STATE_DONE:
    points, ballx, paddlex = parse_outputs(vm.tasks[0].outputs, points, ballx, paddlex)

    joy = 0
    if ballx > paddlex:
        joy = 1
    elif ballx < paddlex:
        joy = -1
    vm.send(vm.tasks[0], joy)
    state = vm.run()

points, ballx, paddlex = parse_outputs(vm.tasks[0].outputs, points, ballx, paddlex)
print(points)
