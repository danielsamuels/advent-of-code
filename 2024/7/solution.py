import functools
import itertools
import operator


class Day:
    def __init__(self, data: str):
        self.data = []
        for line in data.splitlines():
            target, values = line.split(': ')
            self.data.append((int(target), list(map(int, values.split()))))

    def calculate(self, item, part=1) -> int:
        target, values = item
        available_operators = [operator.mul, operator.add]
        if part == 2:
            available_operators.append(lambda x, y: int(f'{x}{y}'))

        permutations = itertools.product(available_operators, repeat=len(values) - 1)

        for operations in permutations:
            operations = list(operations)
            result = functools.reduce(lambda x, y: operations.pop(0)(x, y), values)
            if result == target:
                return target

        return 0

    def run_step_1(self) -> int:
        return sum(self.calculate(item) for item in self.data)

    def run_step_2(self) -> int:
        return sum(self.calculate(item, part=2) for item in self.data)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
