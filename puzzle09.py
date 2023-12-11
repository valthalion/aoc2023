testing = False


def read_data(reverse=False):
    filename = 'puzzle09_test.in' if testing else 'puzzle09.in'
    with open(filename, 'r') as f:
        seqs = tuple(tuple(int(n) for n in line.strip().split()) for line in f)
        if reverse:
            seqs = tuple(seq[::-1] for seq in seqs)
        return seqs


def next_item(seq):
    if all(item == 0 for item in seq):
        return 0
    return seq[-1] + next_item(tuple(a - b for a, b in zip(seq[1:], seq)))


def part_1():
    seqs = read_data()
    return sum(next_item(seq) for seq in seqs)


def part_2():
    seqs = read_data(reverse=True)
    return sum(next_item(seq) for seq in seqs)
