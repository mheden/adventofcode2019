from utils import read_file
from intcode import Intcode, Task
import networkx as nx

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

WALL = 0
CLEAR = 1
OXYGEN = 2
START = 3

dir_to_instr = {
    NORTH: 1,
    SOUTH: 2,
    WEST: 3,
    EAST: 4,
}

dirnames = {
    NORTH: 'north',
    SOUTH: 'south',
    WEST: 'west',
    EAST: 'east'
}

response = {
    WALL: 'wall',
    CLEAR: 'ok',
    OXYGEN: 'oxygen'
}


def update_pos(x, y, dir_):
    DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    dx, dy = DIRS[dir_]
    return x + dx, y + dy


def print_map(map_):
    xs = [x for (x, _) in map_.keys()]
    ys = [y for (_, y) in map_.keys()]
    minx, maxx = min(xs), max(xs)
    miny, maxy = min(ys), max(ys)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            try:
                print("%s" % ['W', ' ', 'o', 'x'][map_[(x, y)]], end='')
            except KeyError:
                print("?", end='')
        print()


program = list(map(int, read_file('15.txt')[0].split(',')))
map_ = {}
map_[(0, 0)] = START
direction = NORTH
G = nx.Graph()

vm = Intcode(verbose=False)
task = Task('part1', program, [], ramsize=4096)
vm.run(task)

oxygenpos = None
x, y = 0, 0
for _ in range(5000):
    vm.send(task, dir_to_instr[direction])
    vm.run(task)
    res = task.outputs.pop(0)
    if res == WALL:
        x_, y_ = update_pos(x, y, direction)
        map_[(x_, y_)] = WALL
        # go right
        direction = (direction + 1) % 4
    elif res == CLEAR:
        x_, y_ = x, y
        x, y = update_pos(x, y, direction)
        G.add_edge((x_, y_), (x, y))
        map_[(x, y)] = CLEAR
        # go left
        direction = (direction + 3) % 4
    elif res == OXYGEN:
        x_, y_ = x, y
        x, y = update_pos(x, y, direction)
        G.add_edge((x_, y_), (x, y))
        map_[(x, y)] = OXYGEN
        oxygenpos = (x, y)
        # go left
        direction = (direction + 3) % 4
# print_map(map_)


print("#--- part1 ---#")

print(nx.shortest_path_length(G, (0, 0), oxygenpos) - 1)


print("#--- part2 ---#")


def process(nodes, fills, seen):
    fills.append(nodes)
    next_ = []
    for node in nodes:
        seen.add(node)
        for n in G.neighbors(node):
            if n not in seen:
                next_.append(n)
    return next_


fills = []
seen = set()
nodes = [oxygenpos]
while True:
    nodes = process(nodes, fills, seen)
    if len(nodes) == 0:
        break
print(len(fills) - 1)
