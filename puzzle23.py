import networkx as nx


testing = False


neighbours = {
    '.': ((-1, 0), (1, 0), (0, -1), (0, 1)),
    '>': ((0, 1),),
    '<': ((0, 1),),
    '^': ((-1, 0),),
    'v': ((1, 0),),
}


def build_graph(cells, use_digraph):
    graph = nx.DiGraph() if use_digraph else nx.Graph()
    for (r, c), value in cells.items():
        for dr, dc in neighbours[value]:
            other_cell = (r + dr, c + dc)
            if other_cell in cells:
                graph.add_edge((r, c), other_cell, weight=1)
    return graph


def collapse(graph):
    while True:
        to_collapse = None
        for node in graph:
            if len(graph[node]) == 2:
                to_collapse = node
                break
        if to_collapse is None:
            break
        new_edge = tuple(graph[node])
        new_weight = sum(graph[node][dest]['weight'] for dest in graph[node])
        graph.remove_node(node)
        graph.add_edge(*new_edge, weight=new_weight)


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
    if ignore_slopes:
        graph = build_graph(cells, use_digraph=False)
        collapse(graph)
    else:
        graph = build_graph(cells, use_digraph=True)
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

    def path_len(path):
        prev = path[0]
        total = 0
        for node in path[1:]:
            total += graph[prev][node]['weight']
            prev = node
        return total

    return max(nx.all_simple_paths(graph, start, end), key=path_len)
