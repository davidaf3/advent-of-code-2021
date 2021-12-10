from functools import reduce

def main():
    with open('input.txt') as f:
        depths = [int(line) for line in f.readlines()]
        print(number_of_increments(depths))

def number_of_increments(depths: list[int]):
    increments = 0
    for i in range(4, len(depths) + 1):
        if sum(depths[i - 3 : i]) > sum(depths[i - 4 : i - 1]):
            increments += 1
    return increments

if __name__ == '__main__':
    main()