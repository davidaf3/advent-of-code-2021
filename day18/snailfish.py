from math import floor, ceil
from functools import reduce


def main():
    with open('input.txt') as f:
        numbers = [eval(line.strip()) for line in f.readlines()]
    print(
        reduce(
            lambda sum, number: sum + number, 
            (SnailfishNumber(number=number) for number in numbers[1:]), 
            SnailfishNumber(number=numbers[0])
        ).magnitude()
    )
    print(
        max(
            (SnailfishNumber(number=numbers[i]) + SnailfishNumber(number=numbers[j])).magnitude() 
            for i in range(len(numbers)) for j in range(len(numbers)) if i != j
        )
    )

class SnailfishNumber(object):

    def __init__(self, number: list = None, left_node: 'SnailfishNumber' = None, 
                 right_node: 'SnailfishNumber' = None, parent: 'SnailfishNumber' = None) -> None:
        self.left, self.right =\
            tuple(
                map(
                    lambda number: RegularNumber(number) if type(number) == int else SnailfishNumber(number), 
                    number
                )
            )\
            if number else (left_node, right_node)
        self.parent: 'SnailfishNumber' = parent
        self.left.parent = self
        self.right.parent = self

    def __add__(self, other: 'SnailfishNumber') -> 'SnailfishNumber':
        result = SnailfishNumber(left_node=self, right_node=other)
        result.reduce()
        return result

    def reduce(self) -> None:
        changed = True
        while changed:
            if not self.explode(0):
                changed = self.split()

    def explode(self, h: int) -> bool:
        if h == 3:
            if not self.left.is_leaf():
                self.right.add_left(self.left.right.value())
                if (left_uncle := self.parent.find_left_uncle(self)):
                    left_uncle.add_right(self.left.left.value())
                self.left = RegularNumber(0)
                return True
            if not self.right.is_leaf():
                self.left.add_right(self.right.left.value())
                if (right_uncle := self.parent.find_right_uncle(self)):
                    right_uncle.add_left(self.right.right.value())
                self.right = RegularNumber(0)
                return True
        return self.left.explode(h + 1) or self.right.explode(h + 1)

    def split(self) -> bool:
        if self.left.is_leaf() and (number := self.left.value()) >= 10:
            self.left = SnailfishNumber(number=[floor(number / 2), ceil(number / 2)], parent=self)
            return True
        if self.left.split():
            return True
        if self.right.is_leaf() and (number := self.right.value()) >= 10:
            self.right = SnailfishNumber(number=[floor(number / 2), ceil(number / 2)], parent=self)
            return True
        return self.right.split()

    def find_left_uncle(self, nephew: 'SnailfishNumber') -> 'SnailfishNumber':
        if self.left != nephew:
            return self.left
        return self.parent.find_left_uncle(self) if self.parent else None

    def find_right_uncle(self, nephew: 'SnailfishNumber') -> 'SnailfishNumber':
        if self.right != nephew:
            return self.right
        return self.parent.find_right_uncle(self) if self.parent else None

    def value(self) -> int:
        return None

    def is_leaf(self) -> bool:
        return False

    def add_right(self, value: int) -> None:
        self.right.add_right(value)

    def add_left(self, value: int) -> None:
        self.left.add_left(value)

    def magnitude(self) -> int:
        return 3 * self.left.magnitude() + 2 * self.right.magnitude()
    
    def __str__(self) -> str:
        return '[' + str(self.left) + ',' + str(self.right) + ']'


class RegularNumber(SnailfishNumber):

    def __init__(self, number: int) -> None:
        self.number = number

    def explode(self, h: int) -> bool:
        return False

    def split(self) -> bool:
        return False
    
    def value(self) -> int:
        return self.number

    def is_leaf(self) -> bool:
        return True

    def add_right(self, value: int) -> None:
        self.number += value

    def add_left(self, value: int) -> None:
        self.number += value

    def magnitude(self) -> int:
        return self.number

    def __str__(self) -> str:
        return str(self.number)


if __name__ == '__main__':
    main()