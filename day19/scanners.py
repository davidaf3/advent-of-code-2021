from itertools import combinations
from functools import reduce
import re


def main():
    regex = re.compile('--- scanner ([0-9]+) ---')
    scanners: list[Scanner] = []
    with open('input.txt') as f:
        while (header := f.readline()):
            n = regex.match(header).group(1)
            scanner_beacons = []
            while (beacon := f.readline().strip()):
                scanner_beacons.append(tuple(map(int, (coord for coord in beacon.strip().split(',')))))
            scanners.append(Scanner(n, scanner_beacons))
    overlapping = {
        (i, j): overlapping 
        for i, j in combinations(range(len(scanners)), 2) 
        if len(overlapping := scanners[i].overlapping_beacons(scanners[j])) >= 12
    }
    transform_coordinates(scanners, 0, overlapping, set())
    beacons: set[tuple[int, int, int]] = set()
    for scanner in scanners:
        for beacon in scanner.beacons:
            beacons.add(beacon)
    print(len(beacons))
    print(
        max(
            map(
                lambda pair: sum(
                    abs(scanners[pair[0]].coordinates[i] - scanners[pair[1]].coordinates[i]) 
                    for i in range(3)
                ), 
                combinations(range(len(scanners)), 2)
            )
        )
    )

def transform_coordinates(scanners: list['Scanner'], index: int, overlapping: dict[tuple[int, int], dict[int, int]], visited: set[int]) -> None:
    visited.add(index)
    next_indexes: set[int] = set()
    for pair in filter(lambda key: index in key, overlapping.keys()):
        reverse = pair[1] == index 
        other = pair[0] if reverse else pair[1]
        if other not in visited:
            scanners[index].relative_coordinates(scanners[other], overlapping[pair], reverse=reverse)
            next_indexes.add(other)
    for next_index in next_indexes:
        transform_coordinates(scanners, next_index, overlapping, visited)

class Scanner(object):

    def __init__(self, n: int, beacons: list[tuple[int, int, int]]) -> None:
        self.n = n
        self.coordinates = (0, 0, 0)
        self.beacons = beacons
        self.differences = {
            (i, j): {abs(beacons[i][k] - beacons[j][k]) for k in range(3)} for i, j in combinations(range(len(beacons)), 2)
        }

    def overlapping_beacons(self, other: 'Scanner') -> dict[int, int]:
        matches: dict[int, int] = {}
        same_differences: dict[tuple[int, int], set[int, int]] = {}
        candidate_beacons_first: set[int] = set()
        for pair_first, diff_first in self.differences.items():
            for pair_second, diff_second in other.differences.items():
                if diff_first == diff_second:
                    same_differences[pair_first] = set(pair_second)
                    candidate_beacons_first.add(pair_first[0])
                    candidate_beacons_first.add(pair_first[1])
                    break
        for beacon in candidate_beacons_first:
            equivalent_pairs = map(
                lambda item: item[1], 
                filter(
                    lambda item: beacon in item[0], 
                    same_differences.items()
                )
            )
            equivalent_beacon = reduce(
                lambda intersection, pair: pair.intersection(intersection), 
                equivalent_pairs, 
                next(equivalent_pairs)
            )
            if len(equivalent_beacon) == 1:
                matches[beacon] = equivalent_beacon.pop()
        return matches

    def relative_coordinates(self, other: 'Scanner', equivalent_beacons: dict[int, int], reverse: bool=False) -> tuple[int, int, int]:
        coordinates_order = [0, 1, 2]
        coordinates_sign = [1, 1, 1]
        equivalent_list = list(equivalent_beacons.items())\
            if not reverse else [tuple(reversed(item)) for item in equivalent_beacons.items()]

        # Find coordinates order
        for first, second in combinations(range(len(equivalent_list)), 2):
            beacon_self_first, beacon_other_first = equivalent_list[first]
            beacon_self_second, beacon_other_second = equivalent_list[second]
            for i in range(3):
                self_difference = self.beacons[beacon_self_first][i] - self.beacons[beacon_self_second][i]
                other_difference = other.beacons[beacon_other_first][i] - other.beacons[beacon_other_second][i]
                if abs(self_difference) != abs(other_difference):
                    coincidences = 0
                    last_coincidence = 0
                    for j in range(3):
                        other_difference = other.beacons[beacon_other_first][j] - other.beacons[beacon_other_second][j]
                        if abs(self_difference) == abs(other_difference):
                            coincidences += 1
                            last_coincidence = j
                    if coincidences == 1:
                        coordinates_order[i] = last_coincidence

        # Find coordinates sign
        for first, second in combinations(range(len(equivalent_list)), 2):
            beacon_self_first, beacon_other_first = equivalent_list[first]
            beacon_self_second, beacon_other_second = equivalent_list[second]
            for i in range(3):
                self_difference = self.beacons[beacon_self_first][i] - self.beacons[beacon_self_second][i]
                other_difference = other.beacons[beacon_other_first][coordinates_order[i]] - other.beacons[beacon_other_second][coordinates_order[i]]
                if self_difference != other_difference:
                    coordinates_sign[i] = -1
        
        other.coordinates = tuple(
            self.beacons[beacon_self_first][i] - other.beacons[beacon_other_first][coordinates_order[i]] * coordinates_sign[i] 
            for i in range(3)
        )

        for beacon in range(len(other.beacons)):
            other.beacons[beacon] = tuple(
                other.beacons[beacon][coordinates_order[coordinate]] * coordinates_sign[coordinate] + other.coordinates[coordinate] 
                for coordinate in range(3)
            )


if __name__ == '__main__':
    main()