from sympy import symbols, solve


testing = False


class Line:
    def __init__(self, start, speed):
        self.start = start
        self.speed = speed

    def cuts_xy(self, line, low, high):
        # x1 + a vx1 = x2 + b vx2
        # y1 + a vy1 = y2 + b vy2

        # a vx1 - b vx2 = x2 - x1
        # a vy1 - b vy2 = y2 - y1

        # a (vx1 - vx1/vy1 vy1) + b (vx1/vy1 vy2 - vx2) = (x2 - x1) - vx1/vy1 (y2 - y1)
        # b = ((x2 - x1) - vx1/vy1 (y2 - y1)) / (vx1/vy1 vy2 - vx2)
        # a = (x2 - x1 + b vx2) / vx1
        x1, y1, _ = self.start
        x2, y2, _ = line.start
        vx1, vy1, _ = self.speed
        vx2, vy2, _ = line.speed

        denom = ((vx1/vy1) * vy2 - vx2)
        if denom == 0:
            return False
        b = ((x2 - x1) - (vx1/vy1) * (y2 - y1)) / denom
        if b < 0:
            return False
        a = (x2 - x1 + b * vx2) / vx1
        if a < 0:
            return False
        x, y = x1 + a * vx1, y1 + a * vy1
        return (low <= x <= high) and (low <= y <= high)

    def __repr__(self):
        return f'<x={self.start}, v={self.speed}>'

def read_data():
    lines = []
    filename = 'puzzle24_test.in' if testing else 'puzzle24.in'
    with open(filename, 'r') as f:
        for line in f:
            start, speed = line.strip().split(' @ ')
            start = tuple(int(n) for n in start.split(', '))
            speed = tuple(int(n) for n in speed.split(', '))
            lines.append(Line(start, speed))
    return lines


def part_1():
    lines = read_data()
    low, high = (7, 27) if testing else (200000000000000, 400000000000000)
    n_lines = len(lines)
    pairs = ((lines[s], lines[p]) for s in range(n_lines - 1) for p in range(s + 1, n_lines))
    return sum(1 for line1, line2 in pairs if line1.cuts_xy(line2, low, high))


def part_2():
    lines = read_data()
    x1, y1, z1 = lines[0].start
    x2, y2, z2 = lines[1].start
    x3, y3, z3 = lines[2].start
    vx1, vy1, vz1 = lines[0].speed
    vx2, vy2, vz2 = lines[1].speed
    vx3, vy3, vz3 = lines[2].speed

    x, y, z = symbols('x'), symbols('y'), symbols('z')
    vx, vy, vz = symbols('vx'), symbols('vy'), symbols('vz')
    sols = solve([
        (x-x1)*(vy-vy1)-(y-y1)*(vx-vx1), (y-y1)*(vz-vz1)-(z-z1)*(vy-vy1), 
        (x-x2)*(vy-vy2)-(y-y2)*(vx-vx2), (y-y2)*(vz-vz2)-(z-z2)*(vy-vy2), 
        (x-x3)*(vy-vy3)-(y-y3)*(vx-vx3), (y-y3)*(vz-vz3)-(z-z3)*(vy-vy3)
        ],
        [x, y, z, vx, vy, vz], dict=True
    )
    # select solution with integer speed components
    for s in sols:
        if s[vx] == int(s[vx]) and s[vy] == int(s[vy]) and s[vz] == int(s[vz]):
            break
    return s[x] + s[y] + s[z]
