
from typing import Pattern, TextIO
from recordclass import RecordClass
import re

def main():
    with open('input.txt') as f:
        drawn_numbers = [int(number) for number in f.readline().strip().split(',')]
        f.readline()

        board_regex = re.compile(' +')
        boards: list['Board'] = []
        while board := readboard(f, board_regex):
            boards.append(board)

    first_board_score = None
    for number in drawn_numbers:
        for board in boards:
            if not board.won:
                board.mark(number)
                if board.won:
                    if not first_board_score:
                        first_board_score = board.score
                    last_board_score = board.score

    print(first_board_score)
    print(last_board_score)

def readboard(f: TextIO, regex: Pattern[str]) -> 'Board':
    numbers = []
    while (line := f.readline()) != '\n':
        if not line:
            return None
        numbers.append([int(number) for number in regex.split(line.strip())])

    return Board(numbers)

class BoardNumber(RecordClass):
    position: tuple[int, int]
    marked: bool

class Board(object):

    def __init__(self, numbers: list[list[int]]) -> None:
        self.won = False
        self.score = 0
        self.size = len(numbers)
        self.lines = [0] * self.size
        self.columns = [0] * self.size
        self.numbers_dict: dict[int, BoardNumber] = {}
        for i in range(self.size):
            for j in range(self.size):
                self.numbers_dict[numbers[i][j]] = BoardNumber((i, j), False)

    def mark(self, number: int) -> None:
        if number in self.numbers_dict:
            self.numbers_dict[number].marked = True
            i, j = self.numbers_dict[number].position
            self.lines[i] += 1
            self.columns[j] += 1
            if self.lines[i] == self.size or self.columns[j] == self.size:
                self.won = True
                self.score = self.get_score(number)

    def get_score(self, number: int) -> int:
        return sum(number for number, info in self.numbers_dict.items() if not info.marked) * number

if __name__ == '__main__':
    main()