BIGNUM = 10**100


def read_file(filename):
    with open(filename) as f:
        lines = f.read().splitlines()
    return lines


def manhattan_distance(a, b):
    x1, y1 = a
    x2, y2 = b
    return abs(x1 - x2) + abs(y1 - y2)
