from typing import Callable
from queue import PriorityQueue
from functools import reduce
from copy import deepcopy
from math import floor


def main():
    types = {
        '.': 0,
        'A': 1,
        'B': 2,
        'C': 3,
        'D': 4
    }
    with open('input.txt') as file:
        file.readline()
        file.readline()
        hallway = [0, 0, 0, 0, 0, 0, 0]
        rooms = [[0, 0], [0, 0], [0, 0], [0, 0]]
        for i in range(2):
            line = file.readline().strip().replace('#', '')
            for j in range(4):
                rooms[j][i] = types[line[j]]
    initial = AmphipodsState(rooms, hallway)
    target = AmphipodsState(
            [[1, 1], [2, 2], [3, 3], [4, 4]],
            [0, 0, 0, 0, 0, 0, 0]
    )
    problem = AmphipodsProblem(initial, target)
    h: Callable[[Node], int] = problem.min_distance_to_target
    f: Callable[[Node], int] = lambda node: node.path_cost
    print(astar(problem, f).path_cost)
    initial.rooms[0] = initial.rooms[0][:-1] + [4, 4] + initial.rooms[0][1:]
    initial.rooms[1] = initial.rooms[1][:-1] + [3, 2] + initial.rooms[1][1:]
    initial.rooms[2] = initial.rooms[2][:-1] + [2, 1] + initial.rooms[2][1:]
    initial.rooms[3] = initial.rooms[3][:-1] + [1, 3] + initial.rooms[3][1:]
    target.rooms = [[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [4, 4, 4, 4]]
    problem = AmphipodsProblem(initial, target)
    print(astar(problem, f).path_cost)

def astar(problem: 'AmphipodsProblem', f: Callable[['Node'], int]) -> 'Node':
    frontier: PriorityQueue[tuple[int, Node]] = PriorityQueue()
    frontier.put((f(problem.initial), problem.initial))
    expanded: set[Node] = set()

    while not frontier.empty():
        _, node = frontier.get()
        expanded.add(node.state)

        if node.state == problem.target:
            return node
        
        for child in problem.expand(node):
            frontier.put((f(child), child))

        while not frontier.empty() and frontier.queue[0][1].state in expanded:
            frontier.get()

    return None

class AmphipodsProblem(object):

    def __init__(self, initial: 'AmphipodsState', target: 'AmphipodsState') -> None:
        self.energy = [1, 10, 100, 1000]
        self.initial = Node(initial, 0, None)
        self.target =  target
    
    def expand(self, node: 'Node') -> list['Node']:
        state = node.state
        children: list[Node] = []
        for i in range(7):
            if state.hallway[i] != 0 and state.is_room_open(state.hallway[i]):
                dst, dir = (state.hallway[i], 1) if i <= state.hallway[i] else (state.hallway[i] + 1, -1)
                if state.is_path_free(i + dir, dst, dir):
                    rooms, hallway = deepcopy(state.rooms), deepcopy(state.hallway)
                    position = state.last_room_position(hallway[i])
                    rooms[hallway[i] - 1][position] = hallway[i]
                    steps = abs(dst - i) * 2 - (1 if i == 0 or i == 6 else 0) + 2 + position
                    cost = node.path_cost + steps * self.energy[hallway[i] - 1]
                    hallway[i] = 0
                    children.append(Node(AmphipodsState(rooms, hallway), cost, node))
        for i in range(4):
            position = state.last_room_position(i + 1) + 1
            if position < len(state.rooms[i]):
                for j in range(7):
                    src, dir = (i + 2, 1) if j >= i + 2 else (i + 1, -1)
                    if state.is_path_free(src, j, dir):
                        rooms, hallway = deepcopy(state.rooms), deepcopy(state.hallway)
                        hallway[j] = rooms[i][position]
                        rooms[i][position] = 0
                        steps = abs(j - src) * 2 - (1 if j == 0 or j == 6 else 0) + 2 + position
                        cost = node.path_cost + steps * self.energy[state.rooms[i][position] - 1]
                        children.append(Node(AmphipodsState(rooms, hallway), cost, node))
                if i != state.rooms[i][position] - 1 and state.is_room_open(state.rooms[i][position]):
                    src, dst, dir = (i + 2, state.rooms[i][position], 1)\
                        if i < state.rooms[i][position] - 1 else (i + 1, state.rooms[i][position] + 1, -1)
                    if state.is_path_free(src, dst, dir):
                        rooms, hallway = deepcopy(state.rooms), deepcopy(state.hallway)
                        dst_position = state.last_room_position(rooms[i][position])
                        rooms[rooms[i][position] - 1][dst_position] = rooms[i][position]
                        rooms[i][position] = 0
                        steps = abs(dst - src) * 2 + 4 + position + dst_position
                        cost = node.path_cost + steps * self.energy[state.rooms[i][position] - 1]
                        children.append(Node(AmphipodsState(rooms, hallway), cost, node))
        return children

    def min_distance_to_target(self, node: 'Node') -> int:
        state = node.state
        distance = 0
        for i in range(7):
            if state.hallway[i] != 0:
                dst = state.hallway[i] if i <= state.hallway[i] else state.hallway[i] + 1
                steps = abs(dst - i) * 2 - (1 if i == 0 or i == 6 else 0) + 1
                distance += steps * self.energy[state.hallway[i] - 1]
        for i in range(4):
            not_in_position = len(node.state.rooms[0])
            for position in range(len(node.state.rooms[0])):
                if i != state.rooms[i][position] - 1:
                    src, dst = (i + 2, state.rooms[i][position])\
                        if i < state.rooms[i][position] - 1 else (i + 1, state.rooms[i][position] + 1)
                    steps = abs(dst - src) * 2 + 3 + position
                    distance += steps * self.energy[state.rooms[i][position] - 1]
            not_in_position = len(node.state.rooms[0])
            last_position = len(node.state.rooms[0]) - 1
            for position in range(len(node.state.rooms[0]) -1, -1, -1):
                if i == state.rooms[i][position] - 1:
                    not_in_position -= 1
                    distance += (last_position - position) * self.energy[i]
                    last_position = last_position + 1
            distance += floor(not_in_position * (not_in_position + 1) / 2) * self.energy[i]
        return distance

class AmphipodsState(object):

    def __init__(self, rooms: list[list[int]], hallway: list[int]) -> None:
        self.rooms = rooms
        self.hallway = hallway

    def is_path_free(self, src: int, dst: int, dir: int) -> bool:
        for i in range(src, dst + dir, dir):
            if self.hallway[i] != 0:
                return False
        return True

    def is_room_open(self, type: int):
        for i in range(len(self.rooms[type - 1]) -1, -1, -1):
            if self.rooms[type - 1][i] != 0 and  self.rooms[type - 1][i] != type:
                return False
        return True

    def last_room_position(self, type: int):
        for i in range(len(self.rooms[type - 1])):
            if self.rooms[type - 1][i] != 0:
                return i - 1
        return len(self.rooms[type - 1]) - 1

    def __eq__(self, __o: object) -> bool:
        return type(__o) == AmphipodsState and __o.rooms == self.rooms and __o.hallway == self.hallway

    def __hash__(self) -> int:
        return hash(str(self.rooms + self.hallway))

class Node(object):

    def __init__(self, state: AmphipodsState, path_cost: int, parent: 'Node') -> None:
        self.state = state
        self.path_cost = path_cost
        self.parent = parent

    def __lt__(self, other: 'Node') -> bool:
        return self.path_cost > other.path_cost


if __name__ == '__main__':
    main()