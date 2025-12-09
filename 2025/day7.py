import collections
from functools import cache
from aocd import data, submit


xdata = """
.......S.......
...............
.......^.......
...............
......^.^......
...............
.....^.^.^.....
...............
....^.^...^....
...............
...^.^...^.^...
...............
..^...^.....^..
...............
.^.^.^.^.^...^.
...............
""".strip()


def part_1():
    rows = data.splitlines()

    current_row: set[int] = set()
    next_row: set[int] = {rows[0].index("S")}

    split_positions = set()

    for row_index, row in enumerate(rows):
        print(f"{row_index=}, {row=}")
        if row_index + 1 == len(rows):
            print(f"Reached the end, exiting")
            continue

        # For each of the rows in the input, determine what index should be used on the row below
        # If you look at the same column on row+1 and it's a `.`, then add it as normal.
        # If the value is instead a '^', then we need to add the indicies either side e.g. 4 becomes 3 and 5.
        current_row, next_row = next_row, set()

        for column_index in current_row:
            # Get the same index from the next row
            value = rows[row_index + 1][column_index]
            print(f"=> {column_index} on next row: {value}")
            if value == ".":
                next_row.add(column_index)
            elif value == "^":
                # Split the column in two
                next_row.add(column_index - 1)
                next_row.add(column_index + 1)
                # Track that the split has occurred
                split_positions.add((row_index + 1, column_index))

    p1_result = len(split_positions)
    print(f"{p1_result=}")
    submit(p1_result, part="a")


@cache
def process_path(
    path: tuple[int],
    next_row_index: int,
    rows: tuple[str],
) -> list[tuple[int]]:
    row_width = len(rows[0])
    partial_paths = []

    # If we're continuing on, look at the value of the next row in the same column index
    column_index = path[-1]
    next_value = rows[next_row_index][column_index]

    if next_value == ".":
        partial_paths.append((*path, column_index))
    elif next_value == "^":
        if column_index > 0:
            partial_paths.append((*path, column_index - 1))

        if column_index < row_width:
            partial_paths.append((*path, column_index + 1))

    return partial_paths


def part_2():
    rows = tuple(data.splitlines())

    total_rows = len(rows)

    # Start with a single path, we'll add more as we go through
    partial_paths = collections.deque([(rows[0].index("S"),)])
    completed_paths = []

    while partial_paths:
        path = partial_paths.pop()
        print(
            f"Working on {path=} ({len(path)}/{total_rows}). {len(partial_paths):,} left to do"
        )

        # If we've reached the bottom, there's nothing left to do
        next_row_index = len(path)
        if next_row_index == total_rows:
            print(f"Completed path: {path=}")
            completed_paths.append(path)
            continue

        new_partial_paths = process_path(path, next_row_index, rows)
        partial_paths.extend(new_partial_paths)

    p2_result = len(completed_paths)
    print(f"{p2_result=}")
    # submit(p2_result, part="b")


def main() -> None:
    # part_1()
    part_2()


if __name__ == "__main__":
    main()
