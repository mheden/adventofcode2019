from utils import read_file
from intcode import Intcode, Task


print("#--- part1 ---#")

program = list(map(int, read_file('09.txt')[0].split(',')))
vm = Intcode()
vm.run(Task('part1', program, [1], ramsize=4096))
print(vm.tasks[0].outputs[0])


print("#--- part2 ---#")

program = list(map(int, read_file('09.txt')[0].split(',')))
vm = Intcode()
vm.run(Task('part2', program, [2], ramsize=4096))
print(vm.tasks[0].outputs[0])
