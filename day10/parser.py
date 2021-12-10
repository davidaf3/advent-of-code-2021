from typing import Generator
from more_itertools import peekable


def main():
    error_score = 0
    complete_scores = []
    with open('input.txt') as f:
        for line in f.readlines():
            parser = Parser(peekable(tokens(line.strip())))
            error_score += parser.error_score
            if parser.complete_score > 0:
                complete_scores.append(parser.complete_score)

    print(error_score)
    print(sorted(complete_scores)[len(complete_scores) // 2])

def tokens(line: str) -> Generator[str, None, None]:
    for token in line:
        yield token
    while True:
        yield None

class Parser(object):

    def __init__(self, tokens: peekable) -> None:
        self.tokens = tokens
        self.error_score = 0
        self.complete_score = 0
        self.complete_scores = {
            ')': 1,
            ']': 2,
            '}': 3,
            '>': 4
        }
        self.error_scores = {
            ')': 3,
            ']': 57,
            '}': 1197,
            '>': 25137
        }
        self.tokens_map = {
            '(': ')',
            '[': ']',
            '{': '}',
            '<': '>'
        }
        while self.error_score == 0 and tokens.peek():
            self.chunk()

    def chunk(self) -> None:
        opening_token = next(self.tokens)
        while self.tokens.peek() in self.tokens_map:
            self.chunk()
            if self.error_score > 0:
                return
        closing_token = next(self.tokens)
        if closing_token != (expected := self.tokens_map[opening_token]):
            if closing_token != None:
                self.error_score = self.error_scores[closing_token]
            else:
                self.complete_score = self.complete_score * 5 + self.complete_scores[expected]
    
if __name__ == '__main__':
    main()