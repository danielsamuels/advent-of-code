from typing import Generator


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def compute_search_indexes_p1(self) -> Generator[tuple, None, None]:
        grid_width = len(self.data[0])
        grid_height = len(self.data)

        # 0..4 -> n-4->n
        for row in range(grid_width):
            for column in range(grid_height):
                yield 'ttb', (column, row), (column, row + 1), (column, row + 2), (column, row + 3)
                yield 'btt', (column, row + 3), (column, row + 2), (column, row + 1), (column, row)
                yield 'ltr', (column, row), (column + 1, row), (column + 2, row), (column + 3, row)
                yield 'rtl', (column + 3, row), (column + 2, row), (column + 1, row), (column, row)
                # Diag, top left to bottom right
                yield 'diag tl-br', (column, row), (column + 1, row + 1), (column + 2, row + 2), (column + 3, row + 3)
                # Diag, bottom left to top right
                yield 'diag bl-tr', (column, row), (column - 1, row + 1), (column - 2, row + 2), (column - 3, row + 3)
                # Diag, top right to bottom left (needed?)
                yield 'diag tr-bl', (column, row), (column + 1, row - 1), (column + 2, row - 2), (column + 3, row - 3)
                # Diag, bottom right to top left (needed?)
                yield 'diag br-tl', (column, row), (column - 1, row - 1), (column - 2, row - 2), (column - 3, row - 3)

    def calculate_p1(self, indexes) -> int:
        style, [ax, ay], [bx, by], [cx, cy], [dx, dy] = indexes
        if any(value < 0 for value in [ax, ay, bx, by, cx, cy, dx, dy]):
            return 0

        try:
            value = self.data[ay][ax] + self.data[by][bx] + self.data[cy][cx] + self.data[dy][dx]
            return value == "XMAS"
        except IndexError:
            return 0

    def run_step_1(self) -> int:
        return sum(self.calculate_p1(indexes) for indexes in self.compute_search_indexes_p1())

    def compute_search_indexes_p2(self) -> Generator[tuple, None, None]:
        grid_width = len(self.data[0])
        grid_height = len(self.data)

        for row in range(grid_width):
            for column in range(grid_height):
                # Assume the given point is the center of the X
                # Yield two tuples, one for each diag
                # Each diag needs to be replicated in each direction
                bl = (row + 1, column - 1)
                br = (row + 1, column + 1)
                tl = (row - 1, column - 1)
                tr = (row - 1, column + 1)
                c = (row, column)

                bltr = (bl, c, tr)
                brtl = (br, c, tl)
                tlbr = (tl, c, br)
                trbl = (tr, c, bl)

                yield bltr, brtl
                yield bltr, tlbr
                yield trbl, brtl
                yield trbl, tlbr


    def calculate_p2(self, indexes) -> int:
        diag1, diag2 = indexes

        [d1ax, d1ay], [d1bx, d1by], [d1cx, d1cy] = diag1
        [d2ax, d2ay], [d2bx, d2by], [d2cx, d2cy] = diag2

        if any(value < 0 for value in [
            d1ax, d1ay, d1bx, d1by, d1cx, d1cy,
            d2ax, d2ay, d2bx, d2by, d2cx, d2cy
        ]):
            return 0

        try:
            s1 = self.data[d1ax][d1ay] + self.data[d1bx][d1by] + self.data[d1cx][d1cy]
            s2 = self.data[d2ax][d2ay] + self.data[d2bx][d2by] + self.data[d2cx][d2cy]
            return s1 == "MAS" and s2 == "MAS"
        except IndexError:
            return 0


    def run_step_2(self) -> int:
        return sum(self.calculate_p2(indexes) for indexes in self.compute_search_indexes_p2())


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
