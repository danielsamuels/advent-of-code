import itertools


class Day:
    def __init__(self, data: str):
        self.data = [
            list(map(int, row.split()))
            for row in data.splitlines()
        ]

    def extrapolate(self, values, history=None):
        if history is None:
            history = [values]

        gaps = [b - a for a, b in itertools.pairwise(values)]
        history = [*history, gaps]

        if not any(gaps):
            return history

        return self.extrapolate(gaps, history)

    def next_value(self, history):
        diff = 0
        for row in reversed(history[:-1]):
            new_value = row[-1] + diff
            diff = new_value

        return new_value

    def run_step_1(self) -> int:
        return sum([
            self.next_value(self.extrapolate(row))
            for row in self.data
        ])

    def run_step_2(self) -> int:
        return sum([
            self.next_value(self.extrapolate(list(reversed(row))))
            for row in self.data
        ])


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
