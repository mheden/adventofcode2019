from utils import read_file, manhattan_distance
from collections import namedtuple


def process_wire(wire):
    x, y = 0, 0
    points = []
    for point in wire.split(','):
        dir_, len_ = point[0], int(point[1:])
        if dir_ == 'U':
            p = [(x, y - d) for d in range(1, len_ + 1)]
            y -= len_
        elif dir_ == 'D':
            p = [(x, y + d) for d in range(1, len_ + 1)]
            y += len_
        elif dir_ == 'L':
            p = [(x - d, y) for d in range(1, len_ + 1)]
            x -= len_
        elif dir_ == 'R':
            p = [(x + d, y) for d in range(1, len_ + 1)]
            x += len_
        points += p
    return points


def calc_dist(wires):
    w0 = set(process_wire(wires[0]))
    w1 = set(process_wire(wires[1]))

    dist = 2**32
    for point in w0.intersection(w1):
        d = manhattan_distance((0, 0), point)
        if d < dist:
            dist = d
    return dist


def calc_steps(wires):
    w0 = process_wire(wires[0])
    w1 = process_wire(wires[1])

    steps = 2**32
    for intersection in set(w0).intersection(set(w1)):
        a = w0.index(intersection) + 1
        b = w1.index(intersection) + 1
        if a + b < steps:
            steps = a + b
    return steps


print("#--- part1 ---#")

assert(calc_dist(["R8,U5,L5,D3", "U7,R6,D4,L4"]) == 6)
assert(calc_dist(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]) == 159)
assert(calc_dist(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]) == 135)

print(calc_dist(read_file('03.txt')))


print("#--- part2 ---#")

assert(calc_steps(["R8,U5,L5,D3", "U7,R6,D4,L4"]) == 30)
assert(calc_steps(["R75,D30,R83,U83,L12,D49,R71,U7,L72", "U62,R66,U55,R34,D71,R55,D58,R83"]) == 610)
assert(calc_steps(["R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51", "U98,R91,D20,R16,D67,R40,U7,R15,U6,R7"]) == 410)

print(calc_steps(read_file('03.txt')))