from utils import read_file
import itertools


class Moon():

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.dx = 0
        self.dy = 0
        self.dz = 0
        self.count = 0

    def __repr__(self):
        return "Moon(step=%d, pos=(%d, %d, %d) spd=(%d, %d, %d))" % (self.count,
                                                                     self.x,
                                                                     self.y,
                                                                     self.z,
                                                                     self.dx,
                                                                     self.dy,
                                                                     self.dz)

    def step(self):
        self.x += self.dx
        self.y += self.dy
        self.z += self.dz
        self.count += 1

    def update_gravity(self, other):
        if self.x > other.x:
            self.dx -= 1
        elif self.x < other.x:
            self.dx += 1
        if self.y > other.y:
            self.dy -= 1
        elif self.y < other.y:
            self.dy += 1
        if self.z > other.z:
            self.dz -= 1
        elif self.z < other.z:
            self.dz += 1

    def energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.dx) + abs(self.dy) + abs(self.dz))


print("#--- part1 ---#")

moons = [
    Moon(19, -10, 7),
    Moon(1, 2, -3),
    Moon(14, -4, 1),
    Moon(8, 7, -6)
]

for _ in range(1000):
    moonlist = moons.copy()
    while len(moonlist) > 0:
        for moon in moonlist[1:]:
            moonlist[0].update_gravity(moon)
            moon.update_gravity(moonlist[0])
        moonlist.pop(0)

    for moon in moons:
        moon.step()

print(sum(m.energy() for m in moons))
