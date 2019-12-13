from utils import read_file
from collections import OrderedDict
from math import degrees, sqrt, atan2


def get_asteroids(map_):
    asteroids = []
    y = 0
    for row in map_:
        for x in [x for x, c in enumerate(row) if c == "#"]:
            asteroids.append((x, y))
        y += 1
    return asteroids


def seen(x, y, asteroids):
    group = {}
    for x_, y_ in asteroids:
        if x == x_ and y == y_:
            continue
        # HACK: add 359.99 instead of 360.0 to make "up" first when sorting
        angle = (degrees(atan2(x - x_, y - y_)) + 359.99) % 360.0
        if angle not in group:
            group[angle] = []
        group[angle].append((sqrt((x - x_) ** 2 + (y - y_) ** 2), x_, y_))
    group_ = OrderedDict()
    for angle in sorted(group, reverse=True):
        group_[angle] = sorted(group[angle])
    return group_


def remove(view):
    removed = []
    len_removed = -1
    while(len(removed) != len_removed):
        len_removed = len(removed)
        for angle in view:
            _, x, y = view[angle].pop(0)
            try:
                removed.append((x, y))
                len_removed += 1
            except IndexError:
                pass
    return removed


print("#--- part1 ---#")

map_ = """.#..#
.....
#####
....#
...##""".splitlines()

asteroids = get_asteroids(map_)
assert(len(seen(1, 0, asteroids)) == 7)
assert(len(seen(4, 0, asteroids)) == 7)
assert(len(seen(0, 2, asteroids)) == 6)
assert(len(seen(1, 2, asteroids)) == 7)
assert(len(seen(2, 2, asteroids)) == 7)
assert(len(seen(3, 2, asteroids)) == 7)
assert(len(seen(4, 2, asteroids)) == 5)
assert(len(seen(4, 3, asteroids)) == 7)
assert(len(seen(3, 4, asteroids)) == 8)
assert(len(seen(4, 4, asteroids)) == 7)

map_ = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".splitlines()

asteroids = get_asteroids(map_)
assert(len(seen(11, 13, asteroids)) == 210)

asteroids = get_asteroids(read_file('10.txt'))
view = []
for y in range(26):
    for x in range(26):
        view.append(len(seen(x, y, asteroids)))
print(max(view))


print("#--- part2 ---#")

map_ = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##""".splitlines()

asteroids = get_asteroids(map_)
view = seen(11, 13, asteroids)
removed = remove(view)

assert(removed[1 - 1] == (11, 12))
assert(removed[2 - 1] == (12, 1))
assert(removed[3 - 1] == (12, 2))
assert(removed[10 - 1] == (12, 8))
assert(removed[20 - 1] == (16, 0))
assert(removed[50 - 1] == (16, 9))
assert(removed[100 - 1] == (10, 16))
assert(removed[199 - 1] == (9, 6))
assert(removed[200 - 1] == (8, 2))

asteroids = get_asteroids(read_file('10.txt'))
view = seen(20, 21, asteroids)
x, y = remove(view)[200 - 1]
print(x * 100 + y)
