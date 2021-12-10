from functools import reduce
import re
from typing import Callable
import numpy as np

def main():
    with open('input.txt') as f:
        report = [np.array([int(digit) for digit in list(line.strip())]) for line in f.readlines()]
        o2_gen = filter_rec(lambda position, most_common: lambda number: most_common == number[position], 0, report)
        co2_scrub = filter_rec(lambda position, most_common: lambda number: most_common != number[position], 0, report)
        print(to_decimal(o2_gen) * to_decimal(co2_scrub))

def filter_rec(filter_fn: Callable[[int, int], Callable[[int], bool]], position: int, numbers: list[np.ndarray]) -> np.ndarray:
    if len(numbers) == 1 or position < 0:
        return numbers[0]
    
    most_common = 1 if sum([number[position] for number in numbers]) >= len(numbers) / 2 else 0
    filtered_numbers = list(filter(filter_fn(position, most_common), numbers))
    return filter_rec(filter_fn, position + 1, filtered_numbers)

def to_decimal(number: np.ndarray) -> int:
    return reduce(lambda decimal, i: decimal + number[i] * 2 ** (len(number) - 1 - i), range(0, len(number)), 0)

if __name__ == '__main__':
    main()