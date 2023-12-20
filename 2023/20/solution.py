from collections import deque, namedtuple, defaultdict

Message = namedtuple('Message', ['source', 'destination', 'signal'])

class Day:
    def __init__(self, data: str):
        modules = {
            # 'output': (None, [], None),
        }

        for line in data.splitlines():
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

    def send_message(self, source, destination, signal):
        self.log.append(f'{source} -{signal}> {destination}')

        if signal == 'low':
            self.low_sent += 1
        else:
            self.high_sent += 1

        self.queue.append(Message(source, destination, signal))

    def calculate(self):
        self.log = []
        self.send_message('button', 'broadcaster', 'low')

        cache = {}

        while self.queue:
            source, this, signal = self.queue.popleft()
            kind, dests, curr = self.modules.get(this, (None, [], None))

            if this == 'rx' and signal == 'low':
                return True

            if kind is None:
                for dest in dests:
                    self.send_message(this, dest, 'low')

            if kind == '%':
                if signal == 'high':
                    continue

                self.modules[this] = (kind, dests, not curr)
                for dest in dests:
                    self.send_message(this, dest, 'low' if curr else 'high')

            if kind == '&':
                # Update the value for this input
                new_value = dict(curr)
                new_value[source] = signal == 'high'
                self.modules[this] = (kind, dests, tuple(new_value.items()))
                all_high = set(new_value.values()) == {True}
                for dest in dests:
                    self.send_message(this, dest, 'low' if all_high else 'high')

    def run_step_1(self) -> int:
        for run in range(1000):
            self.calculate()
            # print(f'Run {run} log:\n', '\n'.join(self.log), f'High: {self.high_sent}, Low: {self.low_sent}')

        return self.low_sent * self.high_sent

    def run_step_2(self) -> int:
        run = 0
        while True:
            run += 1
            if self.calculate():
                return run

        # return sum(self.calculate(item) for item in self.data)
