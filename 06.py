from utils import read_file


def calc_parents(connections, node):
    if node == 'COM':
        return 0
    else:
        return 1 + calc_parents(connections, connections[node])


def get_connections(map_):
    connections = {}
    for line in map_:
        from_, to_ = line.split(')')
        connections[to_] = from_
    return connections


def orbits(map_):
    connections = get_connections(map_)
    return sum([calc_parents(connections, node) for node in connections])


def get_ancestors(connections, node):
    if node == 'COM':
        return [node]
    else:
        return [node] + get_ancestors(connections, connections[node])


def transfers(map_, from_, to_):
    connections = get_connections(map_)
    a = get_ancestors(connections, from_)
    b = get_ancestors(connections, to_)
    common = [i for i in a if i in b][0]
    return (a.index(common) - 1) + (b.index(common) - 1)


print("#--- part1 ---#")

data = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L""".splitlines()

assert(orbits(data) == 42)
print(orbits(read_file('06.txt')))

print("#--- part2 ---#")

data = """COM)B
B)C
C)D
D)E
E)F
B)G
G)H
D)I
E)J
J)K
K)L
K)YOU
I)SAN""".splitlines()

assert(transfers(data, 'YOU', 'SAN') == 4)
print(transfers(read_file('06.txt'), 'YOU', 'SAN'))
