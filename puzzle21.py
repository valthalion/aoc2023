testing = False


def neighbours(cell):
    r, c = cell
    yield (r - 1, c)
    yield (r + 1, c)
    yield (r, c - 1)
    yield (r, c + 1)


def read_data():
    filename = 'puzzle21_test.in' if testing else 'puzzle21.in'
    nodes, start = set(), None
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, cell in enumerate(line.strip()):
                if cell in '.S':
                    nodes.add((r, c))
                    if cell == 'S':
                        start = (r, c)
    graph = {node: {cell for cell in neighbours(node) if cell in nodes} for node in nodes}
    return graph, start


def part_1():
    graph, start = read_data()
    reached = {start}
    for _ in range(6 if testing else 64):
        reached = {n for node in reached for n in graph[node]}
    return len(reached)


def part_2():
    ...
