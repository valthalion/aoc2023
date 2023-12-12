testing = False


def find_type(node, neighbours):
    r, c = node
    if (r + 1, c) in neighbours:
        if (r - 1, c) in neighbours:
            return '|'
        if (r, c - 1) in neighbours:
            return '7'
        if (r, c + 1) in neighbours:
            return 'F'
    if (r - 1, c) in neighbours:
        if (r, c - 1) in neighbours:
            return 'J'
        if (r, c + 1) in neighbours:
            return 'L'
    return '-'


def read_data(test=1):
    filename = f'puzzle10_test{test}.in' if testing else 'puzzle10.in'
    graph = {}
    types = {}
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, value in enumerate(line.strip()):
                if value == '|':
                    graph[(r, c)] = {(r - 1, c), (r + 1, c)}
                    types[(r, c)] = value
                elif value == '-':
                    graph[(r, c)] = {(r, c - 1), (r, c + 1)}
                    types[(r, c)] = value
                elif value == 'L':
                    graph[(r, c)] = {(r - 1, c), (r, c + 1)}
                    types[(r, c)] = value
                elif value == 'J':
                    graph[(r, c)] = {(r - 1, c), (r, c - 1)}
                    types[(r, c)] = value
                elif value == 'F':
                    graph[(r, c)] = {(r + 1, c), (r, c + 1)}
                    types[(r, c)] = value
                elif value == '7':
                    graph[(r, c)] = {(r + 1, c), (r, c - 1)}
                    types[(r, c)] = value
                elif value == 'S':
                    start = (r, c)
    graph[start] = {node for node, neighbours in graph.items() if start in neighbours}
    types[start] = find_type(start, graph[start])
    return start, graph, r, c, types


def connected_component(start, graph):
    comp = set()
    queue = {start}
    nodes = set(graph) - queue
    while queue:
        node = queue.pop()
        neighbours = graph[node] & nodes
        nodes -= neighbours
        queue |= neighbours
        comp.add(node)
    return comp


def part_1():
    start, graph, _, _, _ = read_data()
    loop = connected_component(start, graph)
    return len(loop) // 2


def part_2():
    start, graph, height, width, types = read_data(test=2)
    loop = connected_component(start, graph)

    area = 0
    for r in range(1, height):
        inside = False
        last_corner = None
        for c in range(width):
            node = (r, c)
            if node in loop:
                node_type = types[node]
                if node_type == '|':
                    inside = not inside
                elif node_type in 'FL':
                    last_corner = node_type
                elif node_type == '7':
                    if last_corner == 'L':
                        inside = not inside
                elif node_type == 'J':
                    if last_corner == 'F':
                        inside = not inside
            else:
                if inside:
                    area += 1

    return area
