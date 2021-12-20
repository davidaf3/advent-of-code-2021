
def main():
    with open('input.txt') as f:
        algorithm = f.readline().strip()
        f.readline()
        image = [line.strip() for line in f.readlines()]
    enhancer = ImageEnhancer(image, algorithm)
    for _ in range(2):
        enhancer.enhance()
    print(enhancer.light_pixels())
    for _ in range(48):
        enhancer.enhance()
    print(enhancer.light_pixels())

class ImageEnhancer(object):

    def __init__(self, image: list[str], algorithm: str) -> None:
        self.image = image
        self.algorithm = algorithm
        self.surrounding = '.'

    def enhance(self) -> None:
        output: list[str] = []
        for i in range(len(self.image) + 2):
            output.append('')
            for j in range(len(self.image[0]) + 2):
                output[i] += self.enhance_pixel(i - 1, j - 1)
        self.image = output
        self.surrounding = self.algorithm[0] if self.surrounding == '.' else self.algorithm[511]

    def enhance_pixel(self, x: int, y: int) -> str:
        number, position = 0, 8
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i >= 0 and i < len(self.image) and j >= 0 and j < len(self.image[0]):
                    if self.image[i][j] == '#':
                        number += 2 ** position
                elif self.surrounding == '#':
                    number += 2 ** position
                position -= 1
        return self.algorithm[number]

    def __str__(self) -> str:
        result = ''
        for i in range(len(self.image)):
            for j in range(len(self.image[0])):
                result += self.image[i][j]
            result += '\n'
        return result

    def light_pixels(self) -> int:
        return sum(1 if self.image[i][j] == '#' else 0 for j in range(len(self.image[0])) for i in range(len(self.image)))


if __name__ == '__main__':
    main()