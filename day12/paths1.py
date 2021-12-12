from os import name


def main():
    caves: dict[str, Cave] = {}
    with open('input.txt') as f:
        for line in f.readlines():
            cave_names = line.strip().split('-')
            for cave_name in cave_names:
                if not cave_name in caves:
                    caves[cave_name] = Cave(cave_name)
            caves[cave_names[0]].add_child(caves[cave_names[1]])
            caves[cave_names[1]].add_child(caves[cave_names[0]])
    
    pathfinder = Pathfinder(caves)
    print(len(pathfinder.find_paths('start', 'end')))

class Cave(object):

    def __init__(self, name: str) -> None:
        self.name = name
        self.is_small = name.islower()
        self.children: list[Cave] = []

    def add_child(self, child: 'Cave') -> None:
            self.children.append(child)


class Pathfinder(object):

    def __init__(self, caves: dict[str, Cave]) -> None:
        self.caves = caves


    def find_paths(self, start: str, end: str) -> list[list[str]]:
        paths = []
        small_visited = {cave.name: False for cave in self.caves.values() if cave.is_small}
        self.find_path_rec(self.caves[start], end, [], small_visited, paths)
        return paths

    def find_path_rec(self, start: Cave, end: str, current: list[str], small_visited: dict[str, bool], paths: list[list[str]]) -> None:
        if start.name == end:
            complete_path = [node for node in current]
            complete_path.append(start.name)
            paths.append(complete_path)
            return

        current.append(start.name)
        if start.is_small:
            small_visited[start.name] = True
        
        for child in start.children:
            if not child.is_small or not small_visited[child.name]:
                self.find_path_rec(child, end, current, small_visited, paths)

        current.pop()
        if start.is_small:
            small_visited[start.name] = False

if __name__ == '__main__':
    main()