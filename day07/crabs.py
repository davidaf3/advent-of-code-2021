from typing import Callable
import time

def main():
    with open('input.txt') as f:
        numbers = f.readline()
    crabs = [int(number) for number in numbers.split(',')]
    min_position = min(crabs)
    max_position = max(crabs)
    calculator = FuelCalculator(max_position)
    cost_function1 = lambda x: sum(abs(x - position) for position in crabs)
    cost_function2 = lambda x: sum(calculator.fuel(abs(x - position)) for position in crabs)
    print(find_min(cost_function1, min_position, max_position)[1])
    print(find_min(cost_function2, min_position, max_position)[1])

def find_min(f: Callable[[int], int], start: int, end: int):
    min_x = start
    min_y = f(min_x)
    for x in range(start + 1, end + 1):
        if (y := f(x)) < min_y:
            min_x = x
            min_y = y
    return min_x, min_y

class FuelCalculator(object):

    def __init__(self, max_distance: int) -> None:
        self.memory = [0] * (max_distance + 1)
        for i in range(1, max_distance + 1):
            self.memory[i] = i +  self.memory[i - 1]

    def fuel(self, distance: int):
        return self.memory[distance]

if __name__ == '__main__':
    main()