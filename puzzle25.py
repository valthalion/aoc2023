from math import prod

import networkx as nx


testing = False


def read_data(ignore_slopes=False):
    filename = 'puzzle25_test.in' if testing else 'puzzle25.in'
    graph = nx.Graph()
    with open(filename, 'r') as f:
        for line in f:
            node, neighbours = line.strip().split(': ')
            for other_node in neighbours.split():
                graph.add_edge(node, other_node)
    return graph


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
    graph = read_data()
    groups = nx.community.girvan_newman(graph)
    top_level = next(groups)
    return prod(len(group) for group in top_level)


def part_2():
    pass
