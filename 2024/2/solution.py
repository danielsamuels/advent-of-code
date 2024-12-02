import itertools


class Day:
    def __init__(self, data: str):
        self.data = [list(map(int, item.split())) for item in data.splitlines()]

    def calculate(self, report: list[int]) -> bool:
        all_increasing = True
        all_decreasing = True
        all_safe_changes = True
        for a, b in itertools.pairwise(report):
            if a == b:
                all_increasing = False
                all_decreasing = False
            elif a < b:
                all_decreasing = False
            elif a > b:
                all_increasing = False

            if not (1 <= abs(a - b) <= 3):
                all_safe_changes = False

        return (all_increasing or all_decreasing) and all_safe_changes

    def run_step_1(self) -> int:
        return sum(self.calculate(item) for item in self.data)

    def run_step_2(self) -> int:
        score = 0
        for report in self.data:
            if self.calculate(report):
                score += 1
                continue

            # Try removing a report and see if it can pass
            for x in range(len(report)):
                if self.calculate(report[:x] + report[x + 1:]):
                    score += 1
                    break

        return score


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
