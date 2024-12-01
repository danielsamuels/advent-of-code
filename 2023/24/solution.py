class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def calculate(self, item):
        return 0

    def run_step_1(self) -> int:
        return sum(self.calculate(item) for item in self.data)

    def run_step_2(self) -> int:
        return sum(self.calculate(item) for item in self.data)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
