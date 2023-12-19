from math import prod


testing = True


class Range:
    def __init__(self, **bounds):
        if bounds:
            self.bounds = bounds
        else:
            self.bounds = {feature: (1, 4_000) for feature in 'xmas'}

    @property
    def count(self):
        return prod(hi - lo + 1 for lo, hi in self.bounds.values())

    def split(self, feature, direction, value):
        lo, hi = self.bounds[feature]
        if direction == '>':
            if value < lo:
                return Range(**dict(self.bounds)), None
            if value >= hi:
                return None, Range(**dict(self.bounds))
            else:
                pass_bounds, reject_bounds = dict(self.bounds), dict(self.bounds)
                pass_bounds[feature] = (value + 1, hi)
                reject_bounds[feature] = (lo, value)
                return Range(**pass_bounds), Range(**reject_bounds)
        else:
            if value <= lo:
                return None, Range(**dict(self.bounds))
            if value > hi:
                return Range(**dict(self.bounds)), None
            else:
                pass_bounds, reject_bounds = dict(self.bounds), dict(self.bounds)
                pass_bounds[feature] = (lo, value - 1)
                reject_bounds[feature] = (value, hi)
                return Range(**pass_bounds), Range(**reject_bounds)


def evaluator(feature, cond, value):
    if cond == '>':
        return lambda x: x[feature] > value
    elif cond == '<':
        return lambda x: x[feature] < value
    raise ValueError


def build_workflow(data):
    *conditional_flows, catch_all = data.split(',')
    conditional_flows = [flow.split(':') for flow in conditional_flows]
    conditional_flows = [(evaluator(cond[0], cond[1], int(cond[2:])), dest) for cond, dest in conditional_flows]

    def eval_flow(part):
        for evaluator, dest in conditional_flows:
            if evaluator(part):
                return dest
        return catch_all

    return eval_flow


def read_data():
    filename = 'puzzle19_test.in' if testing else 'puzzle19.in'
    workflows, parts = {}, []
    with open(filename, 'r') as f:
        while True:
            line = next(f).strip()[:-1]
            if not line:
                break
            name, data = line.split('{')
            workflows[name] = build_workflow(data)

        for line in f:
            pairs = line.strip()[1:-1].split(',')
            pairs = [pair.split('=') for pair in pairs]
            parts.append({k: int(v) for k, v in pairs})
    return workflows, parts


def build_workflow2(data):
    *conditional_flows, catch_all = data.split(',')
    conditional_flows = [flow.split(':') for flow in conditional_flows]
    conditional_flows = [((cond[0], cond[1], int(cond[2:])), dest) for cond, dest in conditional_flows]

    def eval_flow(part_range):
        to_process = part_range
        for filter_spec, dest in conditional_flows:
            pass_range, to_process = to_process.split(*filter_spec)
            yield pass_range, dest
        yield to_process, catch_all

    return eval_flow


def read_data2():
    filename = 'puzzle19_test.in' if testing else 'puzzle19.in'
    workflows = {}
    with open(filename, 'r') as f:
        while True:
            line = next(f).strip()[:-1]
            if not line:
                break
            name, data = line.split('{')
            workflows[name] = build_workflow2(data)
    return workflows


def process_part(part, workflows):
    flow = 'in'
    while flow in workflows:
        flow = workflows[flow](part)
    return flow


def process_all(workflows):
    queue = [(Range(), 'in')]
    accepted = []
    while queue:
        r, flow = queue.pop()
        for new_r, new_flow in workflows[flow](r):
            if new_r is not None:
                if new_flow == 'A':
                    accepted.append(new_r)
                    continue
                if new_flow == 'R':
                    continue
                queue.append((new_r, new_flow))
    return sum(r.count for r in accepted)


def part_1():
    workflows, parts = read_data()
    accepted, rejected = set(), set()
    for part in parts:
        result = process_part(part, workflows)
        if result == 'A':
            accepted.add(tuple(part.values()))
        elif result == 'R':
            rejected.add(tuple(part.values()))
        else:
            raise ValueError(result)
    return sum(sum(part) for part in accepted)


def part_2():
    workflows = read_data2()
    return process_all(workflows)
