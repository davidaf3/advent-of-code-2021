import numpy as np


def main():
    with open('input.txt') as f:
        octopuses = Octopueses(np.array([[int(digit) for digit in line.strip()] for line in f.readlines()]))
    i = 0
    while not octopuses.all_flashed:
        octopuses.update()
        i += 1
    print(i)

class Octopueses(object):

    def __init__(self, octopuses: np.ndarray) -> None:
        self.octopuses = octopuses
        self.flashed = [[False for _ in range(len(octopuses))] for _ in range(len(octopuses))]
        self.all_flashed = False

    def update(self) -> None:
        self.increase_energy()
        for i in range(len(self.octopuses)):
            for j in range(len(self.octopuses)):
                if self.octopuses[i][j] > 9 and not self.flashed[i][j]:
                    self.flash(i, j)
        self.reset_flashed()

    def increase_energy(self) -> None:
        self.octopuses += 1

    def flash(self, x: int, y: int) -> None:
        self.flashed[x][y] = True
        for i in range(x - 1, x + 2):
            if i >= 0 and i < len(self.octopuses):
                for j in range(y - 1, y + 2):
                    if (i, j) != (x, y) and j >= 0 and j < len(self.octopuses):
                        self.octopuses[i][j] += 1
                        if self.octopuses[i][j] > 9 and not self.flashed[i][j]:
                            self.flash(i, j)

    def reset_flashed(self) -> None:
        self.all_flashed = True
        for i in range(len(self.octopuses)):
            for j in range(len(self.octopuses)):
                if self.flashed[i][j]:
                    self.flashed[i][j] = False
                    self.octopuses[i][j] = 0
                else:
                    self.all_flashed = False

if __name__ == '__main__':
    main()