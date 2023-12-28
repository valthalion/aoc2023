testing = True


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
    rows, cols = r + 1, c + 1

    def neighbours(cell):
        r, c = cell
        if ((r - 1) % rows, c % cols) in nodes:
            yield (r - 1, c)
        if ((r + 1) % rows, c % cols) in nodes:
            yield (r + 1, c)
        if (r % rows, (c - 1) % cols) in nodes:
            yield (r, c - 1)
        if (r % rows, (c + 1) % cols) in nodes:
            yield (r, c + 1)

    return start, neighbours


def bfs(start, neighbours, steps, history):
    counts = [1]
    reached = {start}

    for _ in range(steps):
        reached = {neighbour for node in reached for neighbour in neighbours(node)}
        counts.append(len(reached))

    return counts if history else counts[-1]


def extrapolate(sequence, steps):
    # f(n) = an^2 + bn + c

    # f(0) = c
    # f(1) = a + b + f0
    # f(2) = 4a + 2b + f0

    # 2a - f0 = f2 - 2f1
    # a = (f2 - 2f1 + f0) / 2

    # (f2 - 2f1 + f0) / 2 + b + f0 = f1
    # b = f1 - f0 - (f2 - 2f1 + f0) / 2

    # f(n) = ((f2 - 2f1 + f0) / 2)n^2 + (f1 - f0 - (f2 - 2f1 + f0) / 2)n + f0
    #      = ((f2 - 2f1 + f0) / 2)n + (f1 - f0 - (f2 - 2f1 + f0) / 2))n + f0
    #      = ((f2 - 2f1 + f0) / 2)(n - 1) + (f1 - f0))n + f0
    #      = f0 + n * (f1 - f0 + (n - 1) * (f2 - 2f1 + f0) / 2)
    cycle_len = 11 if testing else 131
    cycles, remainder = divmod(steps, cycle_len)
    f0, f1, f2, *_ = sequence[remainder::cycle_len]
    return f0 + cycles * (f1 - f0 + (cycles - 1) * (f2 - 2*f1 + f0) // 2)


def part_1():
    start, neighbours = read_data()
    reached = bfs(start, neighbours, steps=6 if testing else 64, history=False)
    return reached


def part_2():
    start, neighbours = read_data()
    reached_at_each_step = bfs(start, neighbours, steps=100 if testing else 600, history=True)
    return extrapolate(reached_at_each_step, steps=5_000 if testing else 26_501_365)
