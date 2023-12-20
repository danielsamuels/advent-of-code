import math
from collections import deque, namedtuple

Message = namedtuple('Message', ['source', 'destination', 'signal'])


class Day:
    def __init__(self, data: str):
        self.data = data

        modules = {}
        for line in self.data.splitlines():
            name, dests = line.split(' -> ')
            dests = dests.split(', ')
            if name == 'broadcaster':
                modules[name] = (None, dests, None)
                continue

            if name[0] == '%':  # Flip flop
                modules[name[1:]] = (name[0], dests, False)
            else:  # Conjunction
                modules[name[1:]] = (name[0], dests, tuple())

        conjunctions = [
            name
            for name, detail in modules.items()
            if detail[0] == '&'
        ]
        for module, (kind, dests, _) in modules.items():
            for dest in dests:
                if dest in conjunctions:
                    t, d, s = modules[dest]
                    modules[dest] = (t, d, (*s, (module, False)))

        # Update all
        self.modules = modules

        self.queue = deque([])
        self.low_sent = 0
        self.high_sent = 0
        self.log = []
        # These all feed into vr at the end, which goes into rx
        # Manual, but oh well
        self.interesting = {
            'pq': None,
            'fg': None,
            'dk': None,
            'fm': None,
        }

    def send_message(self, source, destination, signal):
        # self.log.append(f'{source} -{signal}> {destination}')

        if signal == 'low':
            self.low_sent += 1
        else:
            self.high_sent += 1

        self.queue.append(Message(source, destination, signal))

    def handle_signal(self, iteration, source, this, signal):
        kind, dests, curr = self.modules.get(this, (None, [], None))

        if kind is None:
            for dest in dests:
                self.send_message(this, dest, 'low')

        if kind == '%':
            if signal == 'high':
                return

            self.modules[this] = (kind, dests, not curr)
            for dest in dests:
                self.send_message(this, dest, 'low' if curr else 'high')

        if kind == '&':
            new_value = dict(curr)
            new_value[source] = signal == 'high'

            if this in self.interesting.keys() and signal == 'low':
                if self.interesting[this] is None:
                    self.interesting[this] = iteration

            self.modules[this] = (kind, dests, tuple(new_value.items()))
            all_high = set(new_value.values()) == {True}
            for dest in dests:
                self.send_message(this, dest, 'low' if all_high else 'high')

    def calculate(self, iteration=0):
        self.log = []
        self.send_message('button', 'broadcaster', 'low')

        while self.queue:
            self.handle_signal(iteration, *self.queue.popleft())

        return False, 0

    def run_step_1(self) -> int:
        for run in range(1000):
            self.calculate()
            # print(f'Run {run} log:\n', '\n'.join(self.log), f'\nHigh: {self.high_sent}, Low: {self.low_sent}\n\n')
        return self.low_sent * self.high_sent

    def run_step_2(self) -> int:
        # For each of the broadcast outputs, determine their cycle length
        # Then LCM them!
        run = 0
        while True:
            run += 1

            if not any(v is None for v in self.interesting.values()):
                return math.lcm(*self.interesting.values())

            self.calculate(run)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
