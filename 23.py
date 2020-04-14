from utils import read_file
from intcode import Intcode, Task


print("#--- part1 ---#")

program = list(map(int, read_file('23.txt')[0].split(',')))
vm = Intcode()

tasks = []
for i in range(50):
    task = Task("%d" % i, program, [i], ramsize=20000)
    vm.run(task)
    tasks.append(task)

done = False
result = -1
while not done:
    for i in range(50):
        # print("task %d" % i)
        if len(tasks[i].inputs) == 0:
            # print("\tno msg available -> -1")
            tasks[i].write(-1)
        vm.run(tasks[i])
        data = tasks[i].read()
        while len(data) > 0:
            dest = data.pop(0)
            x = data.pop(0)
            y = data.pop(0)
            # print("\t%d %d -> %d" % (x, y, dest))
            if dest == 255:
                done = True
                result = y
            else:
                tasks[dest].write([x, y])

print(y)
