import re

def main():
    segment_regex = re.compile('([0-9]+),([0-9]+) -> ([0-9]+),([0-9]+)')
    segments: list[Segment] = []

    with open('input.txt') as f:
       for line in f.readlines():
            parsed = segment_regex.match(line)
            x1, y1, x2, y2  = (int(parsed.group(i)) for i in range(1, 5))
            segments.append(Segment(x1, x2, y1, y2))

    overlap_points = set()
    for i in range(len(segments)):
        for j in range(i + 1, len(segments)):
            for point in segments[i].overlap_points(segments[j]):
                overlap_points.add(point)

    print(len(overlap_points))


class Segment(object):

    def __init__(self, x1: int, x2: int, y1: int, y2: int) -> None:
        self.x1, self.x2 = x1, x2
        self.y1, self.y2 = y1, y2
        self.m = (y2 - y1) / (x2 - x1) if x2 - x1 != 0 else None
        self.b = (y1 - self.m * x1) if self.m != None else None
        self.firstx, self.lastx = (x1, x2) if x1 <= x2 else (x2, x1)
        self.firsty, self.lasty = (y1, y2) if y1 <= y2 else (y2, y1)
    
    def overlap_points(self, segment: 'Segment') -> list[tuple[int, int]]:
        # Both vertical and parallel
        if self.m == None and segment.m == None:
            if self.x1 != segment.x1:
                return []
            lower, low_cut, high_cut, higher = sorted([self.y1, self.y2, segment.y1, segment.y2])
            return [(self.x1, y) for y in range(low_cut, high_cut + 1)]\
                if higher - lower <= abs(self.y2 - self.y1) + abs(segment.y2 - segment.y1) else []

        # Parallel
        if self.m == segment.m:
            if self.b != segment.b:
                return []
            first, first_cut, last_cut, last = sorted([(self.x1, self.y1), (self.x2, self.y2), (segment.x1, segment.y1), (segment.x2, segment.y2)],\
                key=lambda point: point[0])
            return [(first_cut[0] + i, int(first_cut[1] + i * self.m)) for i in range(0, last_cut[0] + 1 - first_cut[0])]\
               if last[0] - first[0] <= abs(self.x2 - self.x1) + abs(segment.x2 - segment.x1) else []

        if self.m == None or segment.m == None:
            vertical, other = (self, segment) if self.m == None else (segment, self)
            x = vertical.x1
            y = int(other.m * x + other.b)
        else:
            x = int((segment.b - self.b) / (self.m - segment.m))
            y = int(self.m * x + self.b)

        return[(x, y)] if self.contains(x, y) and segment.contains(x, y) else []

    def contains(self, x: int, y: int) -> bool:  
        if self.m == None:
            return x == self.x1 and y >= self.firsty and y <= self.lasty     
        return y == int(x * self.m + self.b) and x >= self.firstx and x <= self.lastx and y >= self.firsty and y <= self.lasty

if __name__ == '__main__':
    main()