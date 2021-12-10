import re
import numpy as np

def main():
    segment_regex = re.compile('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)')
    segments: list[Segment] = []

    with open('input.txt') as f:
       for line in f.readlines():
            parsed = segment_regex.match(line)
            x1, y1, x2, y2  = (int(parsed.group(i)) for i in range(1, 5))
            if x1 == x2 or y1 == y2:
                segments.append(Segment(x1, x2, y1, y2))

    overlap_points = set()
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            for point in segments[i].overlap_points(segments[j]):
                overlap_points.add(point)

    print(len(overlap_points))


class Segment(object):

    def __init__(self, x1: int, x2: int, y1: int, y2: int) -> None:
        self.x1, self.x2 = (x1, x2) if x1 <= x2 else (x2, x1)
        self.y1, self.y2 = (y1, y2) if y1 <= y2 else (y2, y1)
    
    def overlap_points(self, segment: 'Segment') -> list[tuple[int, int]]:
        # Both vertical
        if self.x1 == self.x2 and segment.x1 == segment.x2:
            if self.x1 != segment.x1:
                return []
            lower, low_cut, high_cut, higher = sorted([self.y1, self.y2, segment.y1, segment.y2])
            return [(self.x1, y) for y in range(low_cut, high_cut + 1)]\
                if higher - lower <= self.y2 - self.y1 + segment.y2 - segment.y1 else []

        # Both horizontal
        if self.y1 == self.y2 and segment.y1 == segment.y2:
            if self.y1 != segment.y1:
                return []
            first, first_cut, last_cut, last = sorted([self.x1, self.x2, segment.x1, segment.x2])
            return [(x, self.y1) for x in range(first_cut, last_cut + 1)]\
                if last - first <= self.x2 - self.x1 + segment.x2 - segment.x1 else []

        # Horizontal and vertical
        x, y = (self.x1, segment.y1) if self.x1 == self.x2 else (segment.x1, self.y1)
        return[(x, y)] if self.contains(x, y) and segment.contains(x, y) else []

    def contains(self, x: int, y: int) -> bool:
        return x >= self.x1 and x <= self.x2 and y >= self.y1 and y <= self.y2

if __name__ == '__main__':
    main()