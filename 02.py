from utils import read_file


def run(ip, lst):
    if lst[ip] == 99:
        return lst
    elif lst[ip] == 1:
        a = lst[lst[ip + 1]]
        b = lst[lst[ip + 2]]
        lst[lst[ip + 3]] = a + b
    elif lst[ip] == 2:
        a = lst[lst[ip + 1]]
        b = lst[lst[ip + 2]]
        lst[lst[ip + 3]] = a * b
    return run(ip + 4, lst)


print("#--- part1 ---#")

assert(run(0, [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
       == [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])
assert(run(0, [1, 0, 0, 0, 99]) == [2, 0, 0, 0, 99])
assert(run(0, [2, 3, 0, 3, 99]) == [2, 3, 0, 6, 99])
assert(run(0, [2, 4, 4, 5, 99, 0]) == [2, 4, 4, 5, 99, 9801])
assert(run(0, [1, 1, 1, 4, 99, 5, 6, 0, 99]) == [30, 1, 1, 4, 2, 5, 6, 0, 99])

values = list(map(int, read_file('02.txt')[0].split(',')))
values[1] = 12
values[2] = 2
print(run(0, values)[0])


print("#--- part2 ---#")

for noun in range(0, 99):
    for verb in range(0, 99):
        values = list(map(int, read_file('02.txt')[0].split(',')))
        values[1] = noun
        values[2] = verb
        if run(0, values)[0] == 19690720:
            print(100 * noun + verb)
            exit(0)
