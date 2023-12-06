from math import ceil, floor, prod, sqrt
from typing import NamedTuple


testing = False


class Race(NamedTuple):
    time: int
    distance: int


def read_data(single_race=False):
    filename = 'puzzle06_test.in' if testing else 'puzzle06.in'
    with open(filename, 'r') as f:
        if single_race:
            time = int(''.join(next(f).strip().split()[1:]))
            distance = int(''.join(next(f).strip().split()[1:]))
            races = Race(time, distance)
        else:
            times = [int(n) for n in next(f).strip().split()[1:]]
            distances = [int(n) for n in next(f).strip().split()[1:]]
            races = [Race(time, distance) for time, distance in zip(times, distances)]
    return races


def winning_range(race):
    aux = sqrt(race.time * race.time - 4 * race.distance)
    min_time = floor((race.time - aux) / 2) + 1
    max_time = ceil((race.time + aux) / 2) - 1
    if min_time > race.time:
        return None, None
    if max_time > race.time:
        max_time = race.time
    return min_time, max_time


def part_1():
    races = read_data()
    ranges = (winning_range(race) for race in races)
    return prod(u - l + 1 for l, u in ranges)


def part_2():
    race = read_data(single_race=True)
    l, u = winning_range(race)
    return u - l + 1
