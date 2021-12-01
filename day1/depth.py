from functools import reduce

def main():
    with open('input.txt') as f:
        depths = [int(line) for line in f.readlines()]
        print(reduce(lambda increments, i: increments + (1 if depths[i] > depths[i - 1] else 0), range(1, len(depths)), 0))

if __name__ == '__main__':
    main()