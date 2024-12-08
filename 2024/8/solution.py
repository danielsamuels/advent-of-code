import itertools
from collections import defaultdict

from utils.grid import Position, compute_new_position


class Day:
    def __init__(self, data: str):
        grid = data.splitlines()
        self.width = len(grid[0])
        self.height = len(grid)

        self.data = defaultdict(list)
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell != '.':
                    self.data[cell].append((x, y))

        self.data = dict(self.data)

    def check_validity(self, location):
        return 0 <= location[0] < self.width and 0 <= location[1] < self.height

    def calculate(self, locations: list[Position], part=1) -> set[Position]:
        valid_locations = set()
        if part == 2:
            valid_locations |= set(locations)

        for a, b in itertools.combinations(locations, 2):
            # (5, 5) + (5, 8) should give (5, 2) and (5, 11)
            x_diff = abs(b[0] - a[0])
            y_diff = abs(b[1] - a[1])

            diff_1 = (-x_diff if a[0] < b[0] else x_diff, -y_diff if a[1] < b[1] else y_diff)
            diff_2 = (x_diff if a[0] < b[0] else -x_diff, y_diff if a[1] < b[1] else -y_diff)

            new_1 = compute_new_position(a, diff_1)
            while self.check_validity(new_1):
                valid_locations.add(new_1)

                if part == 1:
                    break

                new_1 = compute_new_position(new_1, diff_1)

            new_2 = compute_new_position(b, diff_2)
            while self.check_validity(new_2):
                valid_locations.add(new_2)

                if part == 1:
                    break

                new_2 = compute_new_position(new_2, diff_2)

        return valid_locations

    def run_step_1(self) -> int:
        valid_locations = set()
        for location in self.data.values():
            valid_locations |= self.calculate(location)

        return len(valid_locations)

    def run_step_2(self) -> int:
        valid_locations = set()
        for location in self.data.values():
            valid_locations |= self.calculate(location, part=2)

        return len(valid_locations)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
