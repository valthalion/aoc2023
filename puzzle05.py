testing = False


class Interval:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def intersect(self, other):
        if self.start >= other.end or self.end < other.start:
            return None, [self]

        non_intersections = []
        start, end = self.start, self.end
        if self.start < other.start:
            non_intersections.append(Interval(self.start, other.start))
            start = other.start
        if self.end > other.end:
            non_intersections.append(Interval(other.end, self.end))
            end = other.end
        return Interval(start, end), non_intersections

    def move(self, n):
        return Interval(self.start + n, self.end + n)

    def __contains__(self, n):
        return self.start <= n < self.end

    def __repr__(self):
        return f'[{self.start}, {self.end})'

    __str__ = __repr__


class IMap:
    def __init__(self, orig, dest, start2, start1, interval_len):
        self.orig = orig
        self.dest = dest
        self.interval_orig = Interval(start1, start1 + interval_len)
        self.interval_dest = Interval(start2, start2 + interval_len)
        self.delta = start2 - start1

    def __contains__(self, item):
        return item in self.interval_orig

    def convert(self, n):
        return n + self.delta

    def convert_interval(self, interval):
        return interval.move(self.delta)

    def __repr__(self):
        return f'IMap: {self.orig} {self.interval_orig} -> {self.dest} {self.interval_dest}'

    __str__ = __repr__


def read_data(intervals=False):
    filename = 'puzzle05_test.in' if testing else 'puzzle05.in'
    mapgroups = []
    with open(filename, 'r') as f:
        seeds = [int(n) for n in next(f).strip().split(': ')[1].split()]
        if intervals:
            seeds = [Interval(start, start + interval_len) for start, interval_len in zip(seeds[::2], seeds[1::2])]
        next(f)

        eof = False
        while not eof:
            mapgroup = []
            orig, dest = next(f).split()[0].split('-to-')
            for line in f:
                if line == '\n':
                    break
                mapgroup.append(IMap(orig, dest, *(int(n) for n in line.strip().split())))
            else:  # reached EOF: file ended before a blank line
                eof = True
            mapgroups.append(mapgroup)

    return seeds, mapgroups


def convert(mapgroups, n):
    for mapgroup in mapgroups:
        for imap in mapgroup:
            if n in imap:
                n = imap.convert(n)
                break
    return n


def convert_interval(mapgroups, initial_interval):
    intervals = [initial_interval]
    for mapgroup in mapgroups:
        remaining = []
        converted = []
        for imap in mapgroup:
            while intervals:
                interval = intervals.pop()
                intersect, remainder = interval.intersect(imap.interval_orig)
                if intersect is not None:
                    converted.append(imap.convert_interval(intersect))
                remaining.extend(remainder)
            intervals = remaining
            remaining = []
        intervals.extend(converted)
        converted = []
    return min(iv.start for iv in intervals)


def part_1():
    seeds, mapgroups = read_data()
    soils = (convert(mapgroups, seed) for seed in seeds)
    return min(soils)


def part_2():
    seeds, mapgroups = read_data(intervals=True)
    soils = (convert_interval(mapgroups, seed) for seed in seeds)
    return min(soils)
