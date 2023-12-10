from math import lcm


testing = False


def read_data():
    filename = 'puzzle08_test.in' if testing else 'puzzle08.in'
    with open(filename, 'r') as f:
        seq = tuple(1 if c == 'R' else 0 for c in next(f).strip())
        next(f)
        graph = {}
        for line in f:
            orig, left, right = line[:3], line[7:10], line[12:15]
            graph[orig] = (left, right)
    return seq, graph


def repeat(seq):
    while True:
        yield from iter(seq)


def follow(seq, graph, start='AAA'):
    steps, current = 0, start
    for side in repeat(seq):
        current = graph[current][side]
        steps += 1
        if current.endswith('Z'):
            return steps


def multifollow(seq, graph):
    initial_nodes = tuple(node for node in graph if node.endswith('A'))
    cycles = tuple(follow(seq, graph, start=node) for node in initial_nodes)
    return lcm(*cycles)


def part_1():
    seq, graph = read_data()
    return follow(seq, graph)


def part_2():
    seq, graph = read_data()
    return multifollow(seq, graph)
