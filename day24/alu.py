from typing import Callable


def main():
    with open('input.txt') as f:
        program = [line.strip() for line in f.readlines()]
    # I used the generator to try to brute force some values
    #generator = NumberGenerator('11111111111111')
    #alu = ALU(generator.next)
    alu = ALU(input)
    alu.load(program)
    alu.run()

class ALU(object):

    def __init__(self, stdin: Callable[[], str]) -> None:
        self.stdin = stdin
        self.instructions = {
            'inp': self.inp,
            'add': self.add,
            'mul': self.mul,
            'div': self.div,
            'mod': self.mod,
            'eql': self.eql
        }
        self.program: list[str] = []

    def load(self, program: list[str]) -> None:
        self.program = program

    def reset(self) -> None:
        self.ip = 0
        self.registers = {
            'w': 0,
            'x': 0,
            'y': 0,
            'z': 0
        }

    def run(self) -> None:
        self.reset()
        while self.ip < len(self.program):
            instruction = self.program[self.ip].split(' ')
            self.instructions[instruction[0]](*instruction[1:])
            self.ip += 1

    def inp(self, a) -> None:
        self.registers[a] = int(self.stdin())

    def add(self, a: str, b: str) -> None:
        self.registers[a] += self.value(b)

    def mul(self, a: str, b: str) -> None:
        self.registers[a] *= self.value(b)

    def div(self, a: str, b: str) -> None:
        self.registers[a] //= self.value(b)

    def mod(self, a: str, b: str) -> None:
        self.registers[a] %= self.value(b)

    def eql(self, a: str, b: str) -> None:
        self.registers[a] = 1 if  self.registers[a] == self.value(b) else 0

    def value(self, b: str) -> int:
        if b in self.registers:
            return self.registers[b]
        return int(b)

class NumberGenerator(object):

    def __init__(self, reverse: bool, number: str) -> None:
        self.position = 0
        self.reverse_multiplier = -1 if reverse else 1
        self.number = number

    def next(self) -> str:
        if self.position == len(self.number):
            self.number = self.find_next_valid()
            self.position = 0
        next_number = self.number[self.position] 
        self.position += 1
        return next_number

    def find_next_valid(self) -> str:
        number_int = int(self.number) + 1 * self.reverse_multiplier
        number_str = str(number_int)
        while '0' in number_str:
            for i in range(len(number_str)):
                if number_str[i] == '0':
                    number_int += 10 ** (len(number_str) - i - 1) * self.reverse_multiplier
                    number_str = str(number_int)
                    break
        return number_str



if __name__ == '__main__':
    main()