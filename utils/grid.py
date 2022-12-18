import itertools
from typing import Generator

Position = tuple[int, int]


def bridge_points(start: Position, end: Position) -> Generator[Position, None, None]:
    start_x, start_y = start
    diff_x, diff_y = tuple(itertools.starmap(lambda a, b: b - a, zip([start_x, start_y], end)))

    if diff_x != 0:
        step = int(diff_x / abs(diff_x))
        return (
            (new_x, start_y)
            for new_x in range(start_x, start_x + diff_x + step, step)
        )
    elif diff_y != 0:
        step = int(diff_y / abs(diff_y))
        return (
            (start_x, new_y)
            for new_y in range(start_y, start_y + diff_y + step, step)
        )


def bridge_str_points(start: str, end: str) -> Generator[Position, None, None]:
    input_points = (start, end)
    start, end = [tuple(map(int, point.split(','))) for point in input_points]
    return bridge_points(start, end)


def compute_new_position(start: Position, diff: Position) -> Position:
    start_x, start_y = start
    diff_x, diff_y = diff
    return start_x + diff_x, start_y + diff_y


def bridge_diff(start: Position, diff: Position) -> Generator[Position, None, None]:
    end = compute_new_position(start, diff)
    return bridge_points(start, end)


def manhattan_distance(point_a, point_b):
    # Calculate the manhattan distance
    [ax, ay], [bx, by] = point_a, point_b
    return abs(ax - bx) + abs(ay - by)


def print_grid(grid: list[list[int]]):
    populated_char = '@'
    for row in grid:
        if not any(col != 0 for col in row):
            populated_char = '#'

        print('|', ''.join(
            '.' if col == 0
            else populated_char if col == 1
            else '-'
            for col in row
        ), '|')
