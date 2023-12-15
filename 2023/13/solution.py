import copy
import enum


class Traversal(enum.Enum):
    ROW = enum.auto()
    COLUMN = enum.auto()


class Day:
    def __init__(self, data: str):
        self.data = data.split('\n\n')
        self.grids = [
            grid.splitlines()
            for grid in self.data
        ]

    def options(self, dimension):
        window_size = dimension if dimension % 2 == 0 else dimension - 1
        return [
            (offset, window)
            for window in range(window_size, 0, -2)
            for offset in range(dimension - window + 1)
            if offset == 0 or window + offset == dimension
        ]

    def calculate_score(self, rows: list[str], initial=None) -> tuple[int, tuple[Traversal, int, int]] | None:
        row_width, row_height = len(rows[0]), len(rows)
        columns = [[row[x] for row in rows] for x in range(row_width)]

        checks = {
            Traversal.ROW: (self.options(row_width), rows, 1),
            Traversal.COLUMN: (self.options(row_height), columns, 100),
        }
        for traversal, [options, iterator, multiplier] in checks.items():
            for offset, window in options:
                half = offset + window // 2
                if all(item[offset:half] == item[half:offset + window][::-1] for item in iterator):
                    score = half * multiplier
                    result = score, (traversal, offset, window)
                    if result == initial:
                        continue

                    return result

        return None

    def smudge_score(self, grid):
        # Flip a character that lives outside the window to the
        # other type, then see if the values change.
        initial = self.calculate_score(grid)

        row_count, column_count = len(grid), len(grid[0])
        available_cells = [
            (x, y)
            for x in range(column_count)
            for y in range(row_count)
        ]

        for column, row in available_cells:
            new_grid = copy.deepcopy(grid)

            current_row = new_grid[row]
            new_char = '#' if current_row[column] == '.' else '.'
            value = list(current_row)
            value[column] = new_char
            new_value = ''.join(value)

            new_grid[row] = new_value
            new = self.calculate_score(new_grid, initial)
            if new and new != initial:
                return new[0]

        raise Exception('No result found for:\n%s\n(was %s)' % ('\n'.join(grid), initial))

    def run_step_1(self) -> int:
        # 34772
        return sum(self.calculate_score(grid)[0] for grid in self.grids)

    def run_step_2(self) -> int:
        # 35554
        return sum(self.smudge_score(grid) for grid in self.grids)
