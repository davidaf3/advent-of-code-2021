from functools import reduce
from typing import Generator


def main():
    with open('input.txt') as f:
        parser = PacketParser(bits_from_hex(f.readline().strip()))
        result = parser.packet()
        print(parser.version_sum)
        print(result)

def bits_from_hex(hex: str) -> Generator[str, None, None]:
    for digit in hex:
        for bit in bin(int(digit, 16))[2:].zfill(4):
            yield bit

def to_decimal(bits: str) -> int:
    return int(bits, 2)

class PacketParser(object):

    def __init__(self, bit_stream: Generator[str, None, None]) -> None:
        self.bit_stream = bit_stream
        self.version_sum = 0
        self.stream_position = 0
        self.type_functions = {\
            '000': lambda: sum(self.subpackets()),
            '001': lambda: reduce(lambda product, n: product * n, self.subpackets(), 1),
            '010': lambda: min(self.subpackets()),
            '011': lambda: max(self.subpackets()),
            '100': self.literal,
            '101': lambda: 1 if (packets := list(self.subpackets()))[0] > packets[1] else 0,
            '110': lambda: 1 if (packets := list(self.subpackets()))[0] < packets[1] else 0,
            '111': lambda: 1 if (packets := list(self.subpackets()))[0] == packets[1] else 0
        }
        self.length_id_generators = {\
            '0': lambda: self.read_packets_by_length(to_decimal(self.read_bits(15))),
            '1': lambda: (self.packet() for _ in range(to_decimal(self.read_bits(11))))
        }

    def read_bits(self, length: int) -> str:
        self.stream_position += length
        return ''.join(next(self.bit_stream) for _ in range(length))

    def packet(self) -> int:
        self.version_sum += to_decimal(self.read_bits(3))
        return self.type_functions[self.read_bits(3)]()

    def literal(self) -> int:
        bits = ''
        while (group := self.read_bits(5))[0] == '1':
            bits += group[1:]
        return to_decimal(bits + group[1:])

    def subpackets(self) -> Generator[int, None, None]:
        return self.length_id_generators[self.read_bits(1)]()

    def read_packets_by_length(self, length: int) -> Generator[int, None, None]:
        limit = self.stream_position + length
        while self.stream_position < limit:
            yield self.packet()


if __name__ == '__main__':
    main()