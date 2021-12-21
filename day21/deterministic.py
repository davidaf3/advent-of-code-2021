import re


def main():
    regex = re.compile('Player [0-9]+ starting position: ([0-9]+)')
    with open('input.txt') as f:
        positions = [int(regex.match(line.strip()).group(1)) for line in f.readlines()]
    game = Game(positions)     
    while not game.over:
        game.turn()
    print(min(game.scores) * game.dice.rolls)

class DeterministicDice(object):

    def __init__(self) -> None:
        self.rolls = 0
        self.last_roll = 0

    def roll(self) -> int:
        self.rolls += 1
        self.last_roll = self.last_roll % 100 + 1
        return self.last_roll

class Game(object):

    def __init__(self, start: list[int]) -> None:
        self.positions = start
        self.scores = [0, 0]
        self.dice = DeterministicDice()
        self.over = False

    def turn(self) -> None:
        for player in range(len(self.positions)):
            self.positions[player] = (self.positions[player] + sum(self.dice.roll() for _ in range(3)) - 1) % 10 + 1
            self.scores[player] += self.positions[player]
            if self.scores[player] >= 1000:
                self.over = True
                return


if __name__ == '__main__':
    main()