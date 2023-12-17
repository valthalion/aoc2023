testing = False


def read_data():
    filename = 'puzzle16_test.in' if testing else 'puzzle16.in'
    tiles = {}
    with open(filename, 'r') as f:
        for row, line in enumerate(f):
            for col, value in enumerate(line.strip()):
                if value == '.':
                    continue
                tiles[(row, col)] = value
    rows, cols = row + 1, col + 1
    tiles = {complex(c, row - r): value for (r, c), value in tiles.items()}
    return tiles, rows, cols


def run_beam(tiles, rows, cols, initial_pos=None, initial_heading=1):
    if initial_pos is None:
        initial_pos = complex(-1, rows - 1)

    energized = {}
    queue = [(initial_pos, initial_heading)]
    while queue:
        pos, heading = queue.pop()
        while True:
            pos += heading
            if not (0 <= pos.real < cols and 0 <= pos.imag < rows):
                break

            if pos in energized:
                if heading in energized[pos]:  # loop
                    break
                energized[pos].add(heading)
            else:
                energized[pos] = {heading}

            if pos in tiles:
                value = tiles[pos]
                if value == '/':
                    heading *= 1j if heading.real else -1j
                elif value == '\\':
                    heading *= 1j if heading.imag else -1j
                elif value == '-':
                    if heading.imag:
                        queue.append((pos, 1))
                        heading = -1
                elif value == '|':
                    if heading.real:
                        queue.append((pos, 1j))
                        heading = -1j
                else:
                    raise ValueError('Unknown tile', value)
    return energized


def max_beam(tiles, rows, cols):
    start_points = []
    for r in range(rows):
        start_points.append((complex(-1, rows - r - 1), 1))
        start_points.append((complex(cols, rows - r - 1), -1))
    for c in range(cols):
        start_points.append((complex(c, -1), 1j))
        start_points.append((complex(c, rows), -1j))
    return max(
        (
            run_beam(tiles, rows, cols, initial_pos, initial_heading)
            for initial_pos, initial_heading in start_points
        ),
        key=len
    )


def part_1():
    tiles, rows, cols = read_data()
    energy = run_beam(tiles, rows, cols)
    return len(energy)


def part_2():
    tiles, rows, cols = read_data()
    energy = max_beam(tiles, rows, cols)
    return len(energy)
