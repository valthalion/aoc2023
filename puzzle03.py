from math import prod


testing = False


def read_data():
    filename = 'puzzle03_test.in' if testing else 'puzzle03.in'
    parts, symbols = {}, {}
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            building_number = None
            for c, value in enumerate(line.strip()):
                if building_number is None:
                    if value == '.':
                        continue
                    if value.isdigit():
                        building_number = (r, c)
                        parts[building_number] = {'pos': (r, c), 'value': int(value), 'len': 1}
                    else:  # symbol
                        symbols[(r, c)] = value
                else:
                    if value == '.':
                        building_number = None
                        continue
                    if value.isdigit():
                        parts[building_number]['value'] = 10 * parts[building_number]['value'] + int(value)
                        parts[building_number]['len'] += 1
                    else:
                        symbols[(r, c)] = value
                        building_number = None
    return parts, symbols


def part_neighbours(part):
    r, c = part['pos']
    length = part['len']
    return {(r + dr, col) for dr in (-1, 1) for col in range(c - 1, c + length + 1)} | {(r, c - 1), (r, c + length)}


def part_1():
    parts, symbols = read_data()

    def is_valid(part):
        return any(neighbour in symbols for neighbour in part_neighbours(part))

    return sum(part['value'] for part in parts.values() if is_valid(part))


def part_2():
    parts, symbols = read_data()
    gear_positions = set(pos for pos, value in symbols.items() if value == '*')

    gears = {pos: [] for pos in gear_positions}
    for part in parts.values():
        neighbour_symbols = part_neighbours(part) & gear_positions
        for symbol in neighbour_symbols:
            gears[symbol].append(part['value'])
    return sum(prod(gear) for gear in gears.values() if len(gear) == 2)
