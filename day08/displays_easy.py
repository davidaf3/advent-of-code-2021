"""
N sgments   | Digits
2           | 1
3           | 7
4           | 4
6           | 0, 6, 9
5           | 2, 3, 5
7           | 8
"""
import re


def main():
    numbers = 0
    regex = re.compile('([a-g]+( [a-g]+)+) \| ([a-g]+( [a-g]+)+)')
    with open('input.txt') as f:
        for line in f.readlines():
            groups = regex.match(line).groups()
            patterns = groups[0]
            displays = groups[2]
            for display in displays.split(' '):
                if len(display) <= 4 or len(display) == 7:
                    numbers += 1
    print(numbers)

if __name__ == '__main__':
    main()
