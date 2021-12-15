from typing import Callable
from queue import PriorityQueue


def main():
    map: list[list[int]] = []
    with open('input.txt') as f:
        for line in f.readlines():
            map.append([int(number) for number in line.strip()])

    problem = ChitonsProblem(map)
    h: Callable[[Node], int] = lambda node: sum(problem.target[i] - node.state[i] for i in range(len(node.state)))
    f: Callable[[Node], int] = lambda node: node.path_cost + h(node)
    print(astar(problem, f).path_cost)

    for row in range(problem.xmax):
        for i in range(1, 5):
            for number in map[row][:problem.xmax]:
                map[row].append((number + i - 1) % 9 + 1)

    for i in range(1, 5):
        for row in range(problem.xmax):
            map.append([])
            for number in map[row]:
                map[problem.xmax * i + row ].append((number + i - 1) % 9 + 1)

    problem = ChitonsProblem(map)
    h: Callable[[Node], int] = lambda node: sum(problem.target[i] - node.state[i] for i in range(len(node.state)))
    f: Callable[[Node], int] = lambda node: node.path_cost + h(node)
    print(astar(problem, f).path_cost)


def astar(problem: 'ChitonsProblem', f: Callable[['Node'], int]) -> 'Node':
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


class ChitonsProblem(object):

    def __init__(self, map: list[list[int]]) -> None:
        self.map = map
        self.xmax = len(map)
        self.ymax = len(map[self.xmax - 1])
        self.initial = (Node((0, 0), 0, None))
        self.target = (self.xmax - 1, self.ymax - 1)

    def expand(self, node: 'Node') -> list['Node']:
        x, y = node.state
        return [\
            Node(child, node.path_cost + self.map[child[0]][child[1]], node) for child in filter(\
                lambda point: point[0] >= 0 and point[0] < self.xmax and point[1] >= 0 and point[1] < self.ymax, [\
                    (x - 1, y), (x, y - 1), (x, y + 1), (x + 1, y)\
                ]\
            )\
        ]


class Node(object):

    def __init__(self, state: tuple[int, int], path_cost: int, parent: 'Node') -> None:
        self.state = state
        self.path_cost = path_cost
        self.parent = parent

    def __lt__(self, other: 'Node') -> bool:
        return self.path_cost > other.path_cost


if __name__ == '__main__':
    main()