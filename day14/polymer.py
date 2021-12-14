from collections import defaultdict
import re


def main():
    rule_regex = re.compile('([A-Z]+) -> ([A-Z])')
    with open('input.txt') as f:
        template = f.readline().strip()
        rules = {parsed.group(1): parsed.group(2) for line in f.readlines() if (parsed := rule_regex.match(line))}

    elements = defaultdict(lambda: 0)
    polymer = defaultdict(lambda: 0)
    for i in range(len(template) - 1):
        polymer[template[i : i + 2]] += 1
        elements[template[i]] += 1
    elements[template[-1]] += 1

    for _ in range(10):
        step(polymer, rules, elements)
    print(max(elements.values()) - min(elements.values()))
    for _ in range(30):
        step(polymer, rules, elements)
    print(max(elements.values()) - min(elements.values()))

def step(polymer: defaultdict[str, int], rules: dict[str, str], elements: defaultdict[str, int]) -> None:
    initial_pairs = list(polymer.items())
    for pair, n in initial_pairs:
        if pair in rules:
            element = rules[pair]
            elements[element] += n
            polymer[pair] -= n
            polymer[pair[0] + element] += n
            polymer[element + pair[1]] += n

if __name__ == '__main__':
    main()