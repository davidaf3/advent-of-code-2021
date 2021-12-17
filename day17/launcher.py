from math import floor, sqrt
import re


def main():
    with open('input.txt') as f:
        xmin, xmax, ymin, ymax = map(\
            lambda number: int(number),\
            re.search('x=(-?[0-9]+)..(-?[0-9]+), y=(-?[0-9]+)..(-?[0-9]+)', f.readline()).groups()\
        )
    print(triangle_number(-ymin - 1))
    
    configurations = 0
    for x in range(inverse_triangle_number(xmin), xmax + 1):
        for y in range(ymin, -ymin):
            if will_hit_target([x, y], [xmin, ymax], [xmax, ymin]):
                configurations += 1
    print(configurations)

def will_hit_target(init_v: list[int, int], targe_tl: list[int, int], target_br: list[int, int]) -> bool:
    point = [0, 0]
    velocity = init_v
    while point[0] <= target_br[0] and point[1] >= target_br[1]:
        if point[0] >= targe_tl[0] and point[0] <= target_br[0]\
            and point[1] <= targe_tl[1] and point[1] >= target_br[1]:
                return True
        point[0] += velocity[0]
        point[1] += velocity[1]
        if velocity[0] > 0:
            velocity[0] -= 1
        velocity[1] -= 1
    return False

def inverse_triangle_number(n: int) -> int: 
    return floor(sqrt(2 + 2 * n) - 0.5)

def triangle_number(n: int) -> int:
    return floor(n * (n + 1) / 2)

if __name__ == '__main__':
    main()