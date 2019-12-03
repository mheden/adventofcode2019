from utils import read_file, manhattan_distance
from collections import namedtuple


def points_from_wire(wire):
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
    p0 = set(points_from_wire(wires[0]))
    p1 = set(points_from_wire(wires[1]))

    dist = 2**32
    for point in p0.intersection(p1):
        d = manhattan_distance((0, 0), point)
        if d < dist:
            dist = d
    return dist


def calc_steps(wires):
    p0 = points_from_wire(wires[0])
    p1 = points_from_wire(wires[1])

    steps = 2**32
    for intersection in set(p0).intersection(set(p1)):
        a = p0.index(intersection) + 1
        b = p1.index(intersection) + 1
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
