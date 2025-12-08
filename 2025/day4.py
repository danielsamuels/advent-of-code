# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "advent-of-code-data",
# ]
# ///

from pprint import pprint
from aocd import data, submit

from utils.grid import Direction, Position, all_relative_point_occupation, parse_grid


# data = """
# ..@@.@@@@.
# @@@.@.@.@@
# @@@@@.@.@@
# @.@@@@..@.
# @@.@@@@.@@
# .@@@@@@@.@
# .@.@.@.@@@
# @.@@@.@@@@
# .@@@@@@@@.
# @.@.@@@.@.
# """.strip()


def check_grid(grid) -> list[Position]:
    valid_positions = []
    for point in grid:
        occupation = all_relative_point_occupation(grid, point)
        del occupation[Direction.NONE]
        if len(occupation) < 4:
            valid_positions.append(point)

    return valid_positions


def part_1() -> None:
    grid = parse_grid(data)
    p1_result = len(check_grid(grid))

    print(f"{p1_result=}")
    submit(p1_result, part="a")


def part_2() -> None:
    grid = parse_grid(data)
    p2_result = 0

    removables = [(-1, -1)]  # Dummy initialization
    while removables:
        removables = check_grid(grid)
        p2_result += len(removables)

        for removable in removables:
            del grid[removable]

    print(f"{p2_result=}")
    submit(p2_result, part="b")


def main() -> None:
    part_1()
    part_2()


if __name__ == "__main__":
    main()
