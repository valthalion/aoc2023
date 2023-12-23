import networkx as nx


testing = False


class Block:
    def __init__(self, block_id, start, end):
        self.id = block_id
        self.x_start, self.y_start, self.z_start = start
        self.x_end, self.y_end, self.z_end = (n + 1 for n in end)
        self.frozen = self.at_bottom()
        self.potential_supports = None
        self.supports = None

    def drop(self):
        if self.frozen:
            return False
        if self.potential_supports:
            new_z, freeze = max((block.z_end, block.frozen) for block in self.potential_supports)
        else:
            new_z, freeze = 1, True
        delta = self.z_start - new_z
        self.z_start -= delta
        self.z_end -= delta
        self.frozen = freeze
        return True

    def at_bottom(self):
        return self.z_start == 1

    def on_top_of(self, other):
        if other is self:
            return False
        if self.z_start < other.z_end:
            return False
        if self.x_end <= other.x_start or self.x_start >= other.x_end:
            return False
        if self.y_end <= other.y_start or self.y_start >= other.y_end:
            return False
        return True

    def find_potential_supports(self, blocks):
        self.potential_supports = set() if self.at_bottom() else {block for block in blocks if self.on_top_of(block)}

    def find_supports(self):
        if self.at_bottom():
            return
        self.supports = {block.id for block in self.potential_supports if self.z_start == block.z_end}


def read_data():
    blocks = []
    filename = 'puzzle22_test.in' if testing else 'puzzle22.in'
    with open(filename, 'r') as f:
        for idx, line in enumerate(f):
            start, end = (tuple(int(n) for n in point.split(',')) for point in line.strip().split('~'))
            blocks.append(Block(idx, start, end))
    for block in blocks:
        block.find_potential_supports(blocks)
    return blocks


def fall(blocks):
    changes = True
    while changes:
        changes = False
        for block in blocks:
            if block.drop():
                changes = True
    for block in blocks:
        block.find_supports()


def removable_bricks(blocks):
    non_removable = set()
    for block in blocks:
        if block.at_bottom():
            continue
        if len(block.supports) == 1:
            non_removable |= block.supports
    return {block.id for block in blocks} - non_removable


def falls_if_remove(graph, node):
    g = graph.copy()
    g.remove_node(node)
    return len(g) - len(nx.ancestors(g, 'ground')) - 1  # Also remove ground (doesn't fall)


def chain_reaction(blocks):
    graph = nx.DiGraph()
    for block in blocks:
        if block.at_bottom():
            graph.add_edge(block.id, 'ground')
        else:
            for other_block_id in block.supports:
                graph.add_edge(block.id, other_block_id)
    fall_counts = {block.id: falls_if_remove(graph, block.id) for block in blocks}
    return fall_counts


def part_1():
    blocks = read_data()
    fall(blocks)
    return len(removable_bricks(blocks))


def part_2():
    blocks = read_data()
    fall(blocks)
    fall_chains = chain_reaction(blocks)
    return sum(fall_chains.values())
