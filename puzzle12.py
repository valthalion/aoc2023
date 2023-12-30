from functools import cache


testing = False


def compress(pattern):
    last = '.'
    new_pattern = []
    for c in pattern:
        if c == '.' == last:
            continue
        new_pattern.append(c)
        last = c
    while new_pattern and new_pattern[-1] == '.':
        new_pattern.pop()
    return ''.join(new_pattern)


def read_data(extend=False):
    filename = 'puzzle12_test.in' if testing else 'puzzle12.in'
    patterns = []
    with open(filename, 'r') as f:
        for line in f:
            pattern, descriptor = line.strip().split()
            descriptor = tuple(int(n) for n in descriptor.split(','))
            if extend:
                pattern = '?'.join(pattern for _ in range(5))
                descriptor = descriptor * 5
            patterns.append((pattern, descriptor))
    return patterns


def variants(pattern):
    queue = [pattern]
    while queue:
        p = queue.pop()
        idx = p.find('?')
        if idx == -1:
            yield compress(p)
            continue
        queue.append(f'{p[:idx]}#{p[idx+1:]}')
        queue.append(f'{p[:idx]}.{p[idx+1:]}')


def pattern_from_descriptor(descriptor):
    return '.'.join('#' * n for n in descriptor)


def count_combinations_bf(pattern, descriptor):
    descriptor_pattern = pattern_from_descriptor(descriptor)
    return sum(1 for variant in variants(pattern) if variant == descriptor_pattern)


@cache
def count_combinations(pattern, descriptor):
    while pattern and pattern[0] == '.':
        pattern = pattern[1:]

    if len(pattern) < sum(descriptor) + len(descriptor) - 1:
        return 0
    group = descriptor[0]

    if pattern[0] == '?':
        dot_combinations = count_combinations(pattern[1:], descriptor)
        hash_combinations = count_combinations(f'#{pattern[1:]}', descriptor)
        return dot_combinations + hash_combinations

    # pattern[0] == '#'
    if '.' in pattern[1:group]:
        return 0
    if group == len(pattern):
            return 1
    if pattern[group] == '#':
        return 0
    descriptor = descriptor[1:]
    pattern = pattern[group + 1:]  # after group ends assume '.' (only option even for '?' to close group)
    if descriptor:
        return count_combinations(pattern, descriptor)
    return 0 if '#' in pattern else 1


def part_1():
    patterns = read_data()
    combinations = (count_combinations(compress(pattern), descriptor) for pattern, descriptor in patterns)
    return sum(combinations)


def part_2():
    patterns = read_data(extend=True)
    combinations = (count_combinations(compress(pattern), descriptor) for pattern, descriptor in patterns)
    return sum(combinations)
