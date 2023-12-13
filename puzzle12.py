testing = False


def read_data(extend=False):
    filename = 'puzzle12_test.in' if testing else 'puzzle12.in'
    patterns = {}
    with open(filename, 'r') as f:
        for line in f:
            pattern, descriptor = line.strip().split()
            if extend:
                pattern = pattern * 5
            patterns[pattern] = tuple(int(n) for n in descriptor.split(','))
    return patterns


def variants(pattern):
    queue = [pattern]
    while queue:
        p = queue.pop()
        idx = p.find('?')
        if idx == -1:
            yield p
            continue
        queue.append(f'{p[:idx]}#{p[idx+1:]}')
        queue.append(f'{p[:idx]}.{p[idx+1:]}')


def check(pattern, descriptor):
    desc = []
    group = 0
    for c in pattern:
        if c == '#':
            group += 1
        else:
            if group:
                desc.append(group)
                group = 0
    if group:
        desc.append(group)
    return tuple(desc) == descriptor


def count_combinations_bf(pattern, descriptor):
    return sum(1 for variant in variants(pattern) if check(variant, descriptor))


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
    pattern = pattern[group + 1:]  # after gropup ends assume '.' (only option even for '?' to close group)
    if descriptor:
        return count_combinations(pattern, descriptor)
    return 0 if '#' in pattern else 1


def part_1():
    patterns = read_data()
    combinations = (count_combinations_bf(pattern, descriptor) for pattern, descriptor in patterns.items())
    return sum(combinations)


def part_2():
    patterns = read_data(extend=True)
    combinations = (count_combinations(pattern, descriptor) for pattern, descriptor in patterns.items())
    return sum(combinations)
