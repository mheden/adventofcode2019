from utils import read_file
from intcode import Intcode, Task


print("#--- part1 ---#")

program = list(map(int, read_file('19.txt')[0].split(',')))
vm = Intcode()
sum_ = 0
for y in range(0, 50):
    for x in range(0, 50):
        task = Task('part1', program, [x, y], ramsize=4096)
        vm.run(task)
        assert(vm.run(task) == Intcode.STATE_DONE)
        output = task.outputs.pop(0)
        sum_ += output
print(sum_)


print("#--- part2 ---#")

program = list(map(int, read_file('19.txt')[0].split(',')))
vm = Intcode()


def get(x, y):
    task = Task('part1', program, [x, y], ramsize=4096)
    vm.run(task)
    assert(vm.run(task) == Intcode.STATE_DONE)
    return task.outputs.pop(0)


size = 100
offset = (size - 1)
startx, endx = 0, size
y = 10   # the tractor beam looks a bit wierd in the beginning so start a bit further down
result = 0
tractor = {}
done = False
while not done:
    x = startx
    while(get(x, y) == 0):
        x += 1
    startx = x
    x = endx + 2
    while(get(x, y) == 0):
        x -= 1
    endx = x
    tractor[y] = {'startx': startx, 'endx': endx, 'width': endx - startx + 1}

    if y - offset in tractor:
        if tractor[y - offset]['endx'] - tractor[y]['startx'] >= offset:
            result = 10000 * tractor[y]['startx'] + (y - offset)
            done = True
    y += 1
print(result)
