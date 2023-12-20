from collections import deque
from enum import Enum
from math import lcm
from typing import NamedTuple, Optional, Tuple


testing = False


class Pulse(Enum):
    Low = 0
    High = 1


class Queue:
    def __init__(self):
        self.queue = deque()
        self.low_counter = 0
        self.high_counter = 0

    def push(self, msg):
        self.queue.appendleft(msg)
        if msg.pulse == Pulse.High:
            self.high_counter += len(msg.dest)
        else:
            self.low_counter += len(msg.dest)

    def pop(self):
        return self.queue.pop()

    def __bool__(self):
        return len(self.queue) > 0


class Message(NamedTuple):
    source: str
    dest: Optional[Tuple[str, ...]]
    pulse: Pulse


class Module:
    def __init__(self, name, dest, queue):
        self.name = name
        self.dest = dest or None
        self.queue = queue

    def send_pulse(self, pulse):
        if self.dest is not None:
            self.queue.push(Message(self.name, self.dest, pulse))

    def receive_pulse(self, msg):
        self.last_pulse = msg.pulse

    def state(self):
        return (self.name,)

    def __repr__(self):
        return f'{type(self)}({self.name}, {self.dest}, queue)'


class FlipFlop(Module):
    def __init__(self, name, dest, queue):
        super().__init__(name, dest, queue)
        self.current_state = False

    def receive_pulse(self, msg):
        if msg.pulse == Pulse.Low:
            self.current_state = not self.current_state
            self.send_pulse(Pulse.High if self.current_state else Pulse.Low)

    def state(self):
        return(self.name, self.current_state)


class Conjunction(Module):
    def __init__(self, name, dest, queue):
        super().__init__(name, dest, queue)
        self.memory = None
        self.first_memory = None

    def receive_pulse(self, msg):
        self.memory[msg.source] = msg.pulse
        pulse = Pulse.Low if all(p == Pulse.High for p in self.memory.values()) else Pulse.High
        self.send_pulse(pulse)
        if self.first_memory[msg.source] is None and msg.pulse == Pulse.High:
            self.first_memory[msg.source] = 'this iteration'

    def set_origins(self, origins):
        self.memory = {origin: Pulse.Low for origin in origins}
        self.first_memory = {origin: None for origin in self.memory}

    def state(self):
        return (self.name, *tuple(self.memory.values()))


class Broadcaster(Module):
    def receive_pulse(self, msg):
        self.send_pulse(msg.pulse)


def push_button(modules, queue):
    queue.push(Message('button', ('broadcaster',), Pulse.Low))
    while queue:
        msg = queue.pop()
        for dest in msg.dest:
            modules[dest].receive_pulse(msg)


def run_iterations(modules, queue, n):
    for _ in range(n):
        push_button(modules, queue)


def connect_conj_origins(modules):
    conjunctions = (mod for mod, module in modules.items() if isinstance(module, Conjunction))
    for conj in conjunctions:
        modules[conj].set_origins(mod for mod, module in modules.items() if conj in module.dest)


def sinks(modules):
    existing = set(modules)
    dests = {dest for module in modules.values() if module.dest is not None for dest in module.dest}
    return dests - existing


def read_data():
    filename = 'puzzle20_test.in' if testing else 'puzzle20.in'
    queue = Queue()
    modules = {}
    with open(filename, 'r') as f:
        for line in f:
            name, dest = line.strip().split(' -> ')
            dest = tuple(dest.split(', '))
            if name.startswith('&'):
                module_type = Conjunction
                name = name[1:]
            elif name.startswith('%'):
                module_type = FlipFlop
                name = name[1:]
            elif name == 'broadcaster':
                module_type = Broadcaster
            else:
                module_type = Module
            module = module_type(name, dest, queue)
            modules[name] = module
    connect_conj_origins(modules)
    for module in sinks(modules):
        modules[module] = Module(module, None, queue)
    return modules, queue


def part_1():
    modules, queue = read_data()
    run_iterations(modules, queue, 1_000)
    return queue.low_counter * queue.high_counter


def part_2():
    modules, queue = read_data()
    pushed = 0
    trigger = modules['dd'].first_memory
    while True:
        push_button(modules, queue)
        pushed += 1
        for mod in trigger:
            if trigger[mod] == 'this iteration':
                trigger[mod] = pushed
        if all(value is not None for value in trigger.values()):
            return lcm(*trigger.values())
