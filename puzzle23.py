import sys

import networkx as nx


sys.setrecursionlimit(50_000)


testing = False


neighbours = {
    '.': ((-1, 0), (1, 0), (0, -1), (0, 1)),
    '>': ((0, 1),),
    '<': ((0, 1),),
    '^': ((-1, 0),),
    'v': ((1, 0),),
}


def build_graph(cells):
    graph = nx.DiGraph()
    for (r, c), value in cells.items():
        for dr, dc in neighbours[value]:
            other_cell = (r + dr, c + dc)
            if other_cell in cells:
                graph.add_edge((r, c), other_cell)
    return graph


def read_data(ignore_slopes=False):
    filename = 'puzzle23_test.in' if testing else 'puzzle23.in'
    cells = {}
    with open(filename, 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                if value == '#':
                    continue
                cells[(row, col)] = '.' if ignore_slopes else value
    last_row = row
    start, end = None, None
    for r, c in cells:
        if r == 0:
            start = (r, c)
            if end is not None:
                break
        elif r == last_row:
            end = (r, c)
            if start is not None:
                break
    graph = build_graph(cells)
    return graph, start, end


def max_len_path(graph, start, end, visited=frozenset()):
    if start == end:
        return len(visited)

    visited = visited | {start}
    nodes = set(graph.adj[start]) - visited
    best = 0
    for node in nodes:
        new_len = max_len_path(graph, node, end, visited)
        if new_len > best:
            best = new_len
    return best


def part_1():
    graph, start, end = read_data()
    return max(len(path) for path in nx.all_simple_paths(graph, start, end)) - 1  # do not count start


def part_2():
    graph, start, end = read_data(ignore_slopes=True)
    return max_len_path(graph, start, end)
