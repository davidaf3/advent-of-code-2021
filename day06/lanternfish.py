
def main():
    lanternfish = [0] * 7
    babies = [0] * 7
    with open("input.txt") as f:
        for number in f.readline().split(','):
            lanternfish[int(number)] += 1

    for day in range(256):
        update(lanternfish, babies, day)

    print(sum(lanternfish) + sum(babies))

def update(lanternfish: list[int], babies: list[int], day: int) -> None:
    new_children = lanternfish[day % 7]
    lanternfish[(day - 1) % 7] += babies[(day - 1) % 7]
    babies[(day - 1) % 7] = 0
    babies[(day + 2) % 7] += new_children

if __name__ == '__main__':
    main()