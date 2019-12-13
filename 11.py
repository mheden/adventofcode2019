from utils import read_file
from intcode import Intcode, Task


DIR_UP = 0
DIR_RIGHT = 1
DIR_DOWN = 2
DIR_LEFT = 3
NUM_DIRS = 4

COLOR_BLACK = 0
COLOR_WHITE = 1


def run(task, grid):
    x, y, direction = 0, 0, DIR_UP

    vm.send(task, grid[(x, y)])
    state = vm.run()
    while state != Intcode.STATE_DONE:
        color = task.outputs.pop(0)
        turn = task.outputs.pop(0)
        grid[(x, y)] = color

        if turn:
            direction = (direction + 1) % NUM_DIRS
        else:
            direction = (direction + (NUM_DIRS - 1)) % NUM_DIRS

        if direction == DIR_UP:
            y -= 1
        elif direction == DIR_RIGHT:
            x += 1
        elif direction == DIR_DOWN:
            y += 1
        elif direction == DIR_LEFT:
            x -= 1

        if (x, y) in grid:
            color = grid[(x, y)]
        else:
            color = COLOR_BLACK
        vm.send(task, color)
        state = vm.run()
    return grid


print("#--- part1 ---#")

program = list(map(int, read_file('11.txt')[0].split(',')))
vm = Intcode()
task = Task('part1', program, [], ramsize=4096)
vm.load(task)

grid = dict()
grid[(0, 0)] = COLOR_BLACK
print(len(run(task, grid)))


print("#--- part2 ---#")

program = list(map(int, read_file('11.txt')[0].split(',')))
vm = Intcode()
task = Task('part2', program, [], ramsize=4096)
vm.load(task)

grid = dict()
grid[(0, 0)] = COLOR_WHITE
grid = run(task, grid)

for y in range(6):
    for x in range(43):
        try:
            ix = grid[(x, y)]
        except KeyError:
            ix = 0
        print([' ', '\u2588'][ix], end='')
    print()
