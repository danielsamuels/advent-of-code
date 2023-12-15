import enum
import itertools

Matrix = list[list[int]]


class Visible(enum.Enum):
    TOP = enum.auto()
    RIGHT = enum.auto()
    BOTTOM = enum.auto()
    LEFT = enum.auto()


def transform_input(data: str) -> Matrix:
    """
    Transform the string input into a list of lists.

             =>    [
    12345    =>      [1, 2, 3, 4, 5],
    54321    =>      [5, 4, 3, 2, 1],
             =>    ]
    """
    return [
        list(map(int, list(row)))
        for row in data.split('\n')
    ]


def item_visible(data: Matrix, x: int, y: int) -> set[Visible]:
    row = data[y]
    column = [r[x] for r in data]
    cell = row[x]

    visible_from: set[Visible] = set()

    if x == 0:
        visible_from.add(Visible.LEFT)
    if x == len(data[0]) - 1:
        visible_from.add(Visible.RIGHT)
    if y == 0:
        visible_from.add(Visible.TOP)
    if y == len(data) - 1:
        visible_from.add(Visible.BOTTOM)

    # Test left-side visibility
    if all(c < cell for c in row[:x]):
        visible_from.add(Visible.LEFT)

    # Test right-side visibility
    if all(c < cell for c in row[x + 1:]):
        visible_from.add(Visible.RIGHT)

    # Test top visibility
    if all(c < cell for c in column[:y]):
        visible_from.add(Visible.TOP)

    # Test bottom visibility
    if all(c < cell for c in column[y + 1:]):
        visible_from.add(Visible.BOTTOM)

    return visible_from


def visible_items(data: Matrix) -> int:
    rows, columns = len(data), len(data[0])
    coords = itertools.product(range(rows), range(columns))
    return len([
        (x, y)
        for x, y in coords
        if item_visible(data, x, y)
    ])


def calculate_scenic_score(data: Matrix, x: int, y: int) -> int:
    # For a given tree, how far can we get before encountering another
    # tree of the same height?
    row = data[y]
    column = [r[x] for r in data]
    cell = row[x]

    def calculate_score(trees: list[int]) -> int:
        score = 0
        for item in trees:
            score += 1
            if item >= cell:
                break

        return score

    left_score = calculate_score(row[:x][::-1])
    right_score = calculate_score(row[x + 1:])
    top_score = calculate_score(column[:y][::-1])
    bottom_score = calculate_score(column[y + 1:])
    return top_score * right_score * bottom_score * left_score


def calculate_scenic_scores(data: Matrix) -> list[int]:
    rows, columns = len(data), len(data[0])
    coords = itertools.product(range(rows), range(columns))
    return [
        calculate_scenic_score(data, x, y)
        for x, y in coords
    ]


def run_step_1(data: str) -> int:
    return visible_items(transform_input(data))


def run_step_2(data: str) -> int:
    return max(calculate_scenic_scores(transform_input(data)))


if __name__ == "__main__":
    with open(f'data/day_8.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)
