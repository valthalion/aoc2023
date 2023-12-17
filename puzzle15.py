testing = False


def read_data():
    filename = 'puzzle15_test.in' if testing else 'puzzle15.in'
    with open(filename, 'r') as f:
        return next(f).strip().split(',')


def do_hash(txt):
    total = 0
    for c in txt:
        total = ((total + ord(c)) * 17) % 256
    return total


def set_lenses(inputs):
    boxes = {idx: {} for idx in range(256)}
    for txt in inputs:
        if txt[-1] == '-':
            name = txt[:-1]
            box = do_hash(name)
            if name in boxes[box]:
                del boxes[box][name]
        else:
            name, value = txt.split('=')
            value = int(value)
            box = do_hash(name)
            boxes[box][name] = value
    return boxes


def focusing_power(boxes):
    total = 0
    for box, lenses in boxes.items():
        box_value = box + 1
        for pos, focus_len in enumerate(lenses.values(), start=1):
            total += box_value * pos * focus_len
    return total


def part_1():
    inputs = read_data()
    hashes = (do_hash(txt) for txt in inputs)
    return sum(hashes)


def part_2():
    inputs = read_data()
    boxes = set_lenses(inputs)
    return focusing_power(boxes)
