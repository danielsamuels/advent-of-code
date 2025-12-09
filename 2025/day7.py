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


def part_2():
    rows = data.splitlines()
    counts = [0] * len(rows[0])

    for row in rows:
        for index, value in enumerate(row):
            if value == "S":
                counts[index] += 1
            if value == "^":
                counts[index - 1] += counts[index]
                counts[index + 1] += counts[index]
                counts[index] = 0

    p2_result = sum(counts)
    print(f"{p2_result=}")
    submit(p2_result, part="b")


def main() -> None:
    part_1()
    part_2()


if __name__ == "__main__":
    main()
