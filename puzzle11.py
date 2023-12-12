testing = False


def read_data():
    filename = 'puzzle11_test.in' if testing else 'puzzle11.in'
    galaxies = []
    with open(filename, 'r') as f:
        for r, line in enumerate(f):
            for c, value in enumerate(line.strip()):
                if value == '#':
                    galaxies.append((r, c))
    return galaxies


def expand(galaxies, coeff=2):
    rows = {r for r, _ in galaxies}
    cols = {c for _, c in galaxies}

    def distance(p1, p2):
        r1, r2 = sorted(r for r, _ in (p1, p2))
        c1, c2 = sorted(c for _, c in (p1, p2))
        return sum(1 if r in rows else coeff for r in range(r1, r2)) + sum(1 if c in cols else coeff for c in range(c1, c2))

    return distance


def pairwise_distances(distance, galaxies):
    for g1, galaxy1 in enumerate(galaxies[:-1]):
        for galaxy2 in galaxies[g1 + 1:]:
            yield distance(galaxy1, galaxy2)


def part_1():
    galaxies = read_data()
    distance = expand(galaxies)
    return sum(pairwise_distances(distance, galaxies))


def part_2():
    galaxies = read_data()
    distance = expand(galaxies, coeff=100 if testing else 1_000_000)
    return sum(pairwise_distances(distance, galaxies))
