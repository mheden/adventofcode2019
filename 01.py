import math
from utils import read_file


def calc_fuel(mass):
    return math.floor(mass / 3) - 2


def calc_fuel_recursive(mass):
    total = 0
    res = mass
    res = calc_fuel(res)
    while res > 0:
        total += res
        res = calc_fuel(res)
    return total


print("#--- part1 ---#")

assert(calc_fuel(12) == 2)
assert(calc_fuel(14) == 2)
assert(calc_fuel(1969) == 654)
assert(calc_fuel(100756) == 33583)

values = map(int, read_file('01.txt'))
print(sum(map(calc_fuel, values)))


print("#--- part2 ---#")

assert(calc_fuel_recursive(14) == 2)
assert(calc_fuel_recursive(1969) == 966)
assert(calc_fuel_recursive(100756) == 50346)

values = map(int, read_file('01.txt'))
print(sum(map(calc_fuel_recursive, values)))
