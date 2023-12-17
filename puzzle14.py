testing = False


def read_data():
    filename = 'puzzle14_test.in' if testing else 'puzzle14.in'
    with open(filename, 'r') as f:
        table = [list(line.strip()) for line in f]
    return table


def tilt(table):
    rows, cols = len(table), len(table[0])
    for r in range(1, rows):
        for c in range(cols):
            if table[r][c] != 'O':
                continue
            table[r][c] = '.'
            new_r = r
            while True:
                new_r -= 1
                if new_r < 0 or table[new_r][c] != '.':
                    table[new_r + 1][c] = 'O'
                    break


def rotate(table):
    rows, cols = len(table), len(table[0])
    new_table = [[table[rows - r - 1][c] for r in range(rows)] for c in range(cols)]
    return new_table


def tilt_cycle(table):
    for _ in range(4):
        tilt(table)
        table = rotate(table)
    return table


def config(table):
    rows, cols = len(table), len(table[0])
    return tuple((r, c) for r in range(rows) for c in range(cols) if table[r][c] == 'O')


def load(table, rows=None):
    if rows is None:
        rows, cols = len(table), len(table[0])
        return sum(rows - r for r in range(rows) for c in range(cols) if table[r][c] == 'O')
    return sum(rows - r for r, _ in table)


def print_table(table):
    for row in table:
        print(''.join(row))
    print()


def part_1():
    table = read_data()
    tilt(table)
    return load(table)


def part_2():
    target = 1_000_000_000
    table = read_data()
    configs = {config(table): 0}
    for iteration in range(1, target + 1):
        table = tilt_cycle(table)
        new_config = config(table)
        if new_config in configs:
            cycle_start = configs[new_config]
            cycle_len = iteration - cycle_start
            remaining = target - iteration
            position = cycle_start + (remaining % cycle_len)
            # print(cycle_start, cycle_len, remaining, position)
            for conf, i in configs.items():
                if i == position:
                    return load(conf, len(table))
        configs[new_config] = iteration
        # print(iteration, load(new_config, len(table)))
    return load(balls, rows)
