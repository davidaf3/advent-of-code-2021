from functools import reduce
import numpy as np

def main():
    with open('input.txt') as f:
        report = [np.array([int(digit) for digit in list(line.strip())]) for line in f.readlines()]
        most_common = sum(report) // ((len(report) if len(report) % 2 == 0 else len(report) + 1) // 2)
        print(to_decimal(most_common) * to_decimal(1 - most_common))

def to_decimal(number: np.ndarray) -> int:
    return reduce(lambda decimal, i: decimal + number[i] * 2 ** (len(number) - 1 - i), range(0, len(number)), 0)

if __name__ == '__main__':
    main()