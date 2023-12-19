testing = False


headings = {'U': 1j, 'D': -1j, 'R': 1, 'L': -1,3: 1j, 1: -1j, 0: 1, 2: -1}


def read_data(translate=False):
    filename = 'puzzle18_test.in' if testing else 'puzzle18.in'
    with open(filename, 'r') as f:
        for line in f:
            cmd, steps, color = line.strip().split()
            if translate:
                steps, heading = divmod(int(color[2:-1], 16), 16)
                heading = headings[heading]
            else:
                heading = headings[cmd]
                steps = int(steps)
            yield heading, steps


# inspired on https://en.wikipedia.org/wiki/Shoelace_formula
def trench_volume(cmds):
    pos, length, volume = 0, 0, 0
    for heading, steps in cmds:
        if heading.imag == 0:
            volume += pos.imag * steps * heading
        length += steps
        pos += heading * steps
    # inner volume includes border partially
    # count half of each border cell included in straights
    # count 1/4 or 3/4 on corners, depending on orientation
    # globally average of 1/2, as 1/4 and 3/4 corners balance each other
    # except 4 * 1/4 additional to account for the 4 turns to close the shape
    return int(volume) + (length // 2) + 1


def part_1():
    return trench_volume(read_data())

def part_2():
    return trench_volume(read_data(translate=True))
