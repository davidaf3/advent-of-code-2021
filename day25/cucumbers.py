
def main():
    map: list[list[bool]] = []
    herds: list[list['SeaCucumber']] = [[], []]
    with open('input.txt') as f:
        i = 0
        for line in f.readlines():
            map.append([])
            j = 0
            for char in line.strip():
                cucumber_present = char != '.'
                map[i].append(cucumber_present)
                if cucumber_present:
                    herd, direction = (0, (1, 0)) if char == '>' else (1, (0, 1))
                    herds[herd].append(SeaCucumber(*((j, i) + direction)))
                j += 1
            i += 1
    cucumbers = CucumbersMap(map, herds)
    cucumbers.step()
    steps = 1
    while cucumbers.step() != 0:
        steps += 1
    print(steps + 1)

class CucumbersMap(object):

    def __init__(self, map: list[list[bool]], herds: list[list['SeaCucumber']]) -> None:
        self.map = map
        self.herds = herds
        self.ymax = len(map)
        self.xmax = len(map[0])

    def step(self) -> int:
        changed = 0
        for herd in self.herds:
            moving = [cucumber for cucumber in herd if cucumber.can_move(self.map, self.xmax, self.ymax)]
            changed += len(moving)
            for cucumber in moving:
                cucumber.move(self.map)
        return changed

class SeaCucumber(object):

    def __init__(self, x: int, y: int, xdir: int, ydir: int) -> None:
        self.x = x
        self.y = y
        self.xdir = xdir
        self.ydir = ydir
        self.next_move: tuple[int, int] = None

    def can_move(self, map: list[list[bool]], xmax: int, ymax: int) -> bool:
        xnext, ynext = self.x + self.xdir, self.y + self.ydir
        if xnext >= xmax:
            xnext = 0
        if ynext >= ymax:
            ynext = 0
        if not map[ynext][xnext]:
            self.next_move = (xnext, ynext)
            return True
        return False
    
    def move(self, map: list[list[bool]]) -> None:
        if self.next_move:
            map[self.y][self.x] = False
            map[self.next_move[1]][self.next_move[0]] = True
            self.x, self.y = self.next_move
            self.next_move = None


if __name__ == '__main__':
    main()