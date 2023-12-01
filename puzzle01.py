testing = False


digits = ('one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine')
digits_dict = {}
for value, digit in enumerate(digits, start=1):
    start = digit[0]
    if start not in digits_dict:
        digits_dict[start] = {}
    digits_dict[start][digit] = {'len': len(digit), 'value': value}


def read_data(test=None):
    filename = f'puzzle01_test{test}.in' if testing else 'puzzle01.in'
    with open(filename, 'r') as f:
        for line in f:
            yield line.strip()


def decode1(line):
    digits = ''.join(c for c in line if c.isdigit())
    value = ''.join((digits[0], digits[-1]))
    return int(value)


def decode2(line):
    idx = 0
    digits = []
    while idx < len(line):
        c = line[idx]
        if c.isdigit():
            digits.append(int(c))
            idx += 1
        elif c in digits_dict:
            for digit, digit_data in digits_dict[c].items():
                if line[idx : idx + digit_data['len']] == digit:
                    digits.append(digit_data['value'])
                    break
            idx += 1
        else:
            idx += 1
    value = 10 * digits[0] + digits[-1]
    return value


def part_1():
    return sum(decode1(line) for line in read_data(test=1))


def part_2():
    return sum(decode2(line) for line in read_data(test=2))
