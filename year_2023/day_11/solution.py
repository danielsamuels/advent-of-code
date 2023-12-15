import itertools

from utils.data import get_data
from utils.grid import manhattan_distance


class Day:
    def __init__(self, data: str, expansion_amount: int = 1):
        self.locations = self.parse_data(data, expansion_amount)

    def parse_data(self, data, expansion_amount: int):
        data = data.splitlines()
        result = []

        expansion_amount = max(1, expansion_amount - 1)

        # Find the rows and columns which have no galaxies
        empty_rows = []
        empty_columns = set(range(len(data[0])))

        galaxy_locations = []

        for index, values in enumerate(data):
            if all(c == '.' for c in values):
                empty_rows.append(index)
                continue

            for column_index, column in enumerate(values):
                if column == '#':
                    if column_index in empty_columns:
                        empty_columns.remove(column_index)

                    galaxy_locations.append((column_index, index))

        for column in reversed(sorted(empty_columns)):
            for gi, galaxy in enumerate(galaxy_locations):
                if galaxy[0] > column:
                    galaxy_locations[gi] = (galaxy[0] + expansion_amount, galaxy[1])

        for row in reversed(sorted(empty_rows)):
            for gi, galaxy in enumerate(galaxy_locations):
                if galaxy[1] > row:
                    galaxy_locations[gi] = (galaxy[0], galaxy[1] + expansion_amount)

        return galaxy_locations

    def compute_distances(self):
        pairs = itertools.combinations(self.locations, 2)
        return sum(itertools.starmap(manhattan_distance, pairs))

    def run_step_1(self) -> int:
        # 9329143
        return self.compute_distances()

    def run_step_2(self) -> int:
        # 710674907809
        return self.compute_distances()


if __name__ == "__main__":
    data = get_data(__file__)
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data, 1_000_000).run_step_2()}')
