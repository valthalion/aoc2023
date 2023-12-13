testing = False


def read_data():
    filename = 'puzzle13_test.in' if testing else 'puzzle13.in'
    with open(filename, 'r') as f:
        pattern = []
        for line in f:
            if line == '\n':
                yield tuple(pattern)
                pattern = []
                continue
            pattern.append(tuple(1 if c == '#' else 0 for c in line.strip()))
    yield tuple(pattern)


def transpose(pattern):
    return tuple(zip(*pattern))


def find_reflection(pattern):
    n = len(pattern)
    for pos in range(1, n):
        len_to_check = min(pos, n - pos)
        if all(pattern[pos - k - 1] == pattern[pos + k] for k in range(len_to_check)):
            return pos
    return None


def diff(v1, v2):
    return sum(abs(x1 - x2) for x1, x2 in zip(v1, v2))


def find_smudge(pattern):
    n = len(pattern)
    for pos in range(1, n):
        len_to_check = min(pos, n - pos)
        if sum(diff(pattern[pos - k - 1], pattern[pos + k]) for k in range(len_to_check)) == 1:
            return pos
    return None


def score(pattern, find_position=find_reflection):
    vertical_position = find_position(pattern)
    if vertical_position is not None:
        return 100 * vertical_position
    horizontal_position = find_position(transpose(pattern))
    return horizontal_position


def part_1():
    patterns = read_data()
    scores = (score(pattern) for pattern in patterns)
    return sum(scores)


def part_2():
    patterns = read_data()
    scores = (score(pattern, find_position=find_smudge) for pattern in patterns)
    return sum(scores)
