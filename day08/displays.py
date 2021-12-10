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
    total_sum = 0
    regex = re.compile('([a-g]+( [a-g]+)+) \| ([a-g]+( [a-g]+)+)')
    with open('input.txt') as f:
        for line in f.readlines():
            groups = regex.match(line).groups()
            mappings = DisplayMappings(groups[0].split(' '))
            displays = list(reversed(groups[2].split(' ')))
            total_sum += sum(mappings.decode(displays[i]) * 10 ** i for i in range(len(displays)))
    print(total_sum)


class DisplayMappings(object):

    def __init__(self, patterns: list[str]) -> None:
        self.mappings: dict[str, str] = {}
        self.patterns_by_length: dict[int, list[set[str]]]= {}

        for pattern in patterns:
            if len(pattern) in self.patterns_by_length:
                self.patterns_by_length[len(pattern)].append(set(pattern))
            else:
                self.patterns_by_length[len(pattern)] = [set(pattern)]

        self.compute_mappings()
        self.correct_patterns = {
            'abcefg': 0,
            'cf': 1,
            'acdeg': 2,
            'acdfg': 3,
            'bcdf': 4,
            'abdfg': 5,
            'abdefg': 6,
            'acf': 7,
            'abcdefg': 8,
            'abcdfg': 9
        }

    def compute_mappings(self) -> None:
        one = self.patterns_by_length[2][0]
        four = self.patterns_by_length[4][0]
        seven = self.patterns_by_length[3][0]
        eight = self.patterns_by_length[7][0]

        # Top segment, found by comparing 1 and 7
        top = (seven - one).pop()
        self.mappings[top] = 'a'

        # Number 3, found by comparing it to 1
        for pattern in self.patterns_by_length[5]:
            if len(pattern - one) == 3:
                three = pattern

        # Bottom segment, found by comparing 3 and 4
        bottom = (three - four - set(top)).pop()
        self.mappings[bottom] = 'g'

        # Middle segment, found by comparing 3 and 7
        middle = (three - seven - set(bottom)).pop()
        self.mappings[middle] = 'd'

        # Top left segment, found by comparing 4 and 1
        top_left = (four - one - set(middle)).pop()
        self.mappings[top_left] = 'b'

        # Number 5, found with top left segment
        for pattern in self.patterns_by_length[5]:
            if top_left in pattern:
                five = pattern

        # Bottom right, found by comparing 5 and 1
        top_right = (one - five).pop()
        self.mappings[top_right] = 'c'

        # Top right, found by substracting bottom right from 1
        bottom_right = (one - set([top_right])).pop()
        self.mappings[bottom_right] = 'f'

        # Bottom left, found by substracting segments from 8
        bottom_left = (eight - set([top, top_right, top_left, middle, bottom_right, bottom])).pop()
        self.mappings[bottom_left] = 'e'

    def decode(self, display: str) -> int:
        mapped = ''.join(sorted(self.mappings[segment] for segment in display))
        return self.correct_patterns[mapped]

if __name__ == '__main__':
    main()
