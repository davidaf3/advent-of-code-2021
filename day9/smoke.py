from typing import Generator


def main():
    with open('input.txt') as f:
        map = HeightMap([[int(digit) for digit in line.strip()] for line in f.readlines()])
    print(map.total_risk())
    basin_sizes = 1
    for size in list(sorted(map.find_basin_sizes(), reverse=True))[:3]:
        basin_sizes *= size
    print(basin_sizes)
    

class HeightMap(object):

    def __init__(self, map: list[list[int]]) -> None:
        self.map = map
        self.rows = len(map)
        self.columns = len(map[0])
        self.position_filter = lambda position: position[0] >= 0 and position[0] < self.rows\
            and position[1] >= 0 and position[1]  < self.columns

    def total_risk(self) -> int:
        return sum(self.map[i][j] + 1 for i, j in self.find_low_points())

    def find_low_points(self) -> Generator[tuple[int, int], None, None]:
        visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        for i in range(self.rows):
            for j in range(self.columns):
                if self.is_low_point(i, j, visited):
                    yield i, j

    def is_low_point(self, x: int, y: int, visited: list[list[bool]]) -> bool:
        if visited[x][y]:
            return False
        
        height = self.map[x][y]
        for i, j in filter(self.position_filter, [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]):
            if self.map[i][j] < height:
                return False
            visited[i][j] = True
            if self.map[i][j] == height:
                return False
        return True

    def find_basin_sizes(self) -> Generator[int, None, None]:
        visited = [[False for _ in range(self.columns)] for _ in range(self.rows)]
        for i, j in self.find_low_points():
            yield self.basin_size(i, j, visited)

    def basin_size(self, x: int, y: int, visited: list[list[bool]]) -> int:
        visited[x][y] = True
        return sum(\
            self.basin_size(i, j, visited) for i, j in filter(\
                self.position_filter, [(x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)]\
            ) if not visited[i][j] and self.map[i][j] >= self.map[x][y] and self.map[i][j] < 9\
        ) + 1

             
if __name__ == '__main__':
    main()