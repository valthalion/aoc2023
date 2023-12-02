from math import prod


testing = False


def read_data():
    filename = 'puzzle02_test.in' if testing else 'puzzle02.in'
    games = {}
    with open(filename, 'r') as f:
        for line in f:
            game, plays = line.strip().split(': ')
            game_id = int(game.split()[1])
            cubes = {cube: 0 for cube in ('red', 'green', 'blue')}
            for play in plays.split('; '):
                shown = play.split(', ')
                for sample in shown:
                    num, colour = sample.split()
                    num = int(num)
                    if num > cubes[colour]:
                        cubes[colour] = num
                games[game_id] = cubes
    return games


def valid(cubes, test_bag):
    return all(num <= test_bag[colour] for colour, num in cubes.items())


def power(cubes):
    return prod(cubes.values())


def part_1():
    games = read_data()
    test_bag = {'red': 12, 'green': 13, 'blue': 14}
    return sum(game_id for game_id, cubes in games.items() if valid(cubes, test_bag))


def part_2():
    games = read_data()
    return sum(power(cubes) for cubes in games.values())
