def main():
    submarine = Submarine()
    with open("input.txt") as f:
        command_list = [((words := line.split(' '))[0], int(words[1])) for line in f.readlines()]
        submarine.move(command_list)
        print(submarine.horizontal_position * submarine.depth)

class Submarine(object):

    def __init__(self) -> None:
        self.depth = 0
        self.horizontal_position = 0
        self.aim = 0
        self.commands = {
            'forward': self.forward,
            'down': self.down,
            'up': self.up
        }

    def forward(self, x: int):
        self.horizontal_position += x
        self.depth += self.aim * x

    def down(self, x: int):
        self.aim += x

    def up(self, x: int):
        self.aim -= x

    def move(self, command_list: list[tuple[str, int]]):
        for command, x in command_list:
            self.commands[command](x)


if __name__ == '__main__':
    main()