import re


def main():
    with open('input.txt') as f:
        dots = set()
        while (line := f.readline()) != '\n':
            dots.add(tuple([int(number) for number in line.strip().split(',')]))
        paper = Paper(dots)
        regex = re.compile('fold along ([a-z])=([0-9]+)')
        first_fold = True
        for line in f.readlines():
            axis, coordinate = regex.match(line).groups()
            paper.fold(ord(axis) - 120, int(coordinate))
            if first_fold:
                print(len(paper.dots))
                first_fold = False
        print_paper(paper)
    
def print_paper(paper: 'Paper') -> None:
    max_x = max(paper.dots, key=lambda dot: dot[0])[0]
    max_y = max(paper.dots, key=lambda dot: dot[1])[1]
    for j in range(max_y + 1):
        for i in range(max_x + 1):
            print('#' if (i, j) in paper.dots else '.', end='')
        print()

class Paper(object):

    def __init__(self, dots: set[tuple[int, int]]) -> None:
        self.dots = dots

    def fold(self, axis: int, coordinate: int) -> None:
        dots_to_fold = list(filter(lambda dot: dot[axis] > coordinate, self.dots))
        for dot in dots_to_fold:
            self.dots.remove(dot)
            folded_dot = list(dot)
            folded_dot[axis] -= 2 * (dot[axis] - coordinate)
            self.dots.add(tuple(folded_dot))


if __name__ == '__main__':
    main()