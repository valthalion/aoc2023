from functools import cache

import networkx as nx


testing = False


def read_data():
    filename = 'puzzle17_test.in' if testing else 'puzzle17.in'
    plan = {}
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, value in enumerate(line.strip()):
                plan[complex(c, r)] = int(value)
    return plan, r, c


def convert_plan(plan, min_steps=1, max_steps=3):
    max_steps += 1
    graph = nx.DiGraph()
    for node in plan:
        for heading, direction in ((1, 'hor'), (-1, 'hor'), (1j, 'ver'), (-1j, 'ver')):
            acc_heat_loss = 0
            for steps in range(1, max_steps):
                pos = node + steps * heading
                if pos not in plan:
                    break
                acc_heat_loss += plan[pos]
                if steps >= min_steps:
                    graph.add_edge((node, direction), (pos, ('hor' if direction == 'ver' else 'ver')), weight=acc_heat_loss)
    return graph


def find_path(graph, orig, dest):
    graph.add_edge(orig, (orig, 'ver'), weight=0)
    graph.add_edge(orig, (orig, 'hor'), weight=0)
    graph.add_edge((dest, 'ver'), dest, weight=0)
    graph.add_edge((dest, 'hor'), dest, weight=0)
    return nx.shortest_path_length(graph, orig, dest, weight='weight')


def part_1():
    plan, last_row, last_col = read_data()
    graph = convert_plan(plan)
    orig, dest = 0, complex(last_col, last_row)
    return find_path(graph, orig, dest)


def part_2():
    plan, last_row, last_col = read_data()
    graph = convert_plan(plan, min_steps=4, max_steps=10)
    orig, dest = 0, complex(last_col, last_row)
    return find_path(graph, orig, dest)
