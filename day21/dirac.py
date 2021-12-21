import re


def main():
    regex = re.compile('Player [0-9]+ starting position: ([0-9]+)')
    with open('input.txt') as f:
        positions = [int(regex.match(line.strip()).group(1)) for line in f.readlines()]
    game = Game(positions)
    game.turn(0)
    print(max(game.won))
    
class Game(object):

    def __init__(self, start: list[int, int]) -> None:
        self.positions = start
        self.scores = [0, 0]
        self.won = [0, 0]
        self.universes = 1
        self.universes_by_result = [1, 3, 6, 7, 6, 3, 1]

    def turn(self, player: int) -> None:
        if max(self.scores) >= 21:
            self.won[0 if self.scores[0] > self.scores[1] else 1] += self.universes
            return

        for result in range(3, 10):
            old_position = self.positions[player]
            old_score = self.scores[player]
            old_universes = self.universes
            self.positions[player] = (self.positions[player] + result - 1) % 10 + 1
            self.scores[player] += self.positions[player]
            self.universes *= self.universes_by_result[result - 3]
            self.turn((player + 1) % 2)
            self.positions[player] = old_position
            self.scores[player] = old_score
            self.universes = old_universes


if __name__ == '__main__':
    main()