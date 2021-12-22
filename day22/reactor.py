from functools import reduce
import re


def main():
    regex = re.compile('(on|off) x=(-?[0-9]+)..(-?[0-9]+),y=(-?[0-9]+)..(-?[0-9]+),z=(-?[0-9]+)..(-?[0-9]+)')
    reactor = Reactor()
    actions = {
        'on': reactor.turn_on,
        'off': reactor.turn_off
    }
    initialization = True
    with open('input.txt') as f:
        for line in f.readlines():
            instruction = regex.match(line).groups()
            coords = tuple(map(int, instruction[1:]))
            if initialization and min(coords[1:]) < -50 and max(coords[1:]) > 50:
                print(reactor.count_on())
                initialization = False
            actions[instruction[0]](Cuboid(*coords))
    print(reactor.count_on())

class Reactor(object):

    def __init__(self) -> None:
        self.cuboids_on: list[Cuboid] = []

    def turn_on(self, cuboid: 'Cuboid') -> None:
        self.turn_off(cuboid)
        self.cuboids_on.append(cuboid)

    def turn_off(self, cuboid: 'Cuboid') -> None:
        for other in self.cuboids_on:
            if other.is_overlapping(cuboid):
                other.exclude_overlapping(cuboid)

    def count_on(self) -> int:
        return sum(cuboid.count() for cuboid in self.cuboids_on)

class Cuboid(object):

    def __init__(self, xmin: int, xmax: int, ymin: int, ymax: int, zmin: int, zmax: int) -> None:
        self.min = (xmin, ymin, zmin)
        self.max = (xmax, ymax, zmax)
        self.excluded: list[Cuboid] = []

    def is_overlapping(self, other: 'Cuboid') -> bool:
        for i in range(3):
            if not (self.min[i] <= other.min[i] and self.max[i] >= other.min[i] or\
                    self.min[i] >= other.min[i] and self.min[i] <= other.max[i]):
                return False
        return True

    def exclude_overlapping(self, other: 'Cuboid') -> None:
        for cuboid in self.excluded:
            if cuboid.is_overlapping(other):
                cuboid.exclude_overlapping(other)
        self.excluded.append(self.overlapping_cuboid(other))

    def overlapping_cuboid(self, other: 'Cuboid') -> 'Cuboid':
        return Cuboid(*sum(
            (
                ((self.min[i], other.max[i]) if self.max[i] >= other.max[i]\
                    else (self.min[i], self.max[i]))\
                if self.min[i] >= other.min[i] else\
                ((other.min[i], self.max[i]) if self.max[i] <= other.max[i]\
                    else (other.min[i], other.max[i]))
                for i in range(3)
            ), ()
        ))

    def count(self) -> int:
        return reduce(
            lambda product, i: product * (self.max[i] + 1 - self.min[i]), 
            (i for i in range(3)),
            1
        ) - sum(cuboid.count() for cuboid in self.excluded)

if __name__ == '__main__':
    main()