import enum
import itertools
from collections import defaultdict
from typing import Generator, Optional, Union

Position = tuple[int, int]
Grid = dict[Position, str]

# sqrt(tiles / 6) = edge length


class Direction(Position, enum.Enum):
    NORTHWEST = (-1, -1)
    NORTH = (0, -1)
    NORTHEAST = (1, -1)
    SOUTHWEST = (-1, 1)
    SOUTH = (0, 1)
    SOUTHEAST = (1, 1)
    WEST = (-1, 0)
    EAST = (1, 0)


class Connection(tuple[Position], enum.Enum):
    START = []

    VERTICAL = (Direction.NORTH, Direction.SOUTH)
    HORIZONTAL = (Direction.EAST, Direction.WEST)

    NORTHEAST = (Direction.SOUTH, Direction.WEST)
    SOUTHEAST = (Direction.NORTH, Direction.WEST)

    NORTHWEST = (Direction.SOUTH, Direction.EAST)
    SOUTHWEST = (Direction.NORTH, Direction.EAST)


def bridge_points(start: Position, end: Position) -> Generator[Position, None, None]:
    start_x, start_y = start
    diff_x, diff_y = tuple(itertools.starmap(lambda a, b: b - a, zip([start_x, start_y], end)))

    if diff_x != 0 and diff_y != 0:
        step_x = int(diff_x / abs(diff_x))
        step_y = int(diff_y / abs(diff_y))

        def next_value():
            range_x = iter(range(start_x, start_x + diff_x + step_x, step_x))
            range_y = iter(range(start_y, start_y + diff_y + step_y, step_y))

            x, y = start_x, start_y
            take_x = False
            while (x, y) != end:
                if take_x:
                    try:
                        x = next(range_x)
                    except StopIteration:
                        y = next(range_y)

                else:
                    try:
                        y = next(range_y)
                    except StopIteration:
                        x = next(range_x)

                take_x = not take_x
                yield x, y

        return (
            (new_x, new_y)
            for new_x, new_y in next_value()
            if (new_x, new_y) not in [start, end]
        )

    if diff_x != 0:
        step = int(diff_x / abs(diff_x))
        return (
            (new_x, start_y)
            for new_x in range(start_x, start_x + diff_x + step, step)
            if (new_x, start_y) not in [start, end]
        )

    if diff_y != 0:
        step = int(diff_y / abs(diff_y))
        return (
            (start_x, new_y)
            for new_y in range(start_y, start_y + diff_y + step, step)
            if (start_x, new_y) not in [start, end]
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


def print_grid(grid: list[list[int]], *, populated_char=None, borders=True):
    if populated_char is None:
        populated_char = '#'

    print()
    for row in grid:
        middle = ''.join(
            '.' if col is None else populated_char if populated_char else col
            for col in row
        )
        if borders:
            print('|', middle, '|')
        else:
            print(middle)


def find_in_grid(grid, target, x_hint=None, y_hint=None) -> Position:
    for y, row in enumerate(grid):
        if y_hint is not None and y != y_hint:
            continue

        for x, cell in enumerate(row):
            if x_hint is not None and x != x_hint:
                continue

            if cell == target:
                return x, y


def parse_grid(
        data: [list, str],
        mapping: Optional[bool | dict] = None,
        *,
        ignore_dots: bool = False,
        merge_contiguous: type = None,
) -> dict:
    """Take a string and turn it into a dict"""
    DROP = object()

    if mapping is None:
        mapping = {
            '.': DROP,
            '#': 1,
        }

    if isinstance(data, str):
        data = data.splitlines()

    grid = defaultdict(int)
    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == '.' and ignore_dots:
                continue

            if mapping is not False:
                value = mapping.get(value, 1)

            if value == DROP:
                continue

            grid[(x, y)] = value

    return grid


def relative_points_occupied(grid: dict, position: Position, directions: list[Direction]) -> list[bool]:
    return [
        grid.get(compute_new_position(position, direction), False)
        for direction in directions
    ]


def all_relative_point_occupation(grid: dict, position: Position) -> dict[Direction, dict]:
    """From a given point, which directions are occupied?"""
    result = {}
    for direction in Direction:
        point = compute_new_position(position, direction)
        if point_val := grid.get(point):
            result[direction] = {
                'position': point,
                'value': point_val
            }

    return result

def get_contiguous_value(grid: Grid, position: Position):
    """From a given position, find the start and end point of a string"""
    start_point = position
    result = grid.get(start_point)

    while (position := compute_new_position(position, Direction.WEST)) and (value := grid.get(position)):
        if value.isdigit():
            result = value + result

    position = start_point
    while (position := compute_new_position(position, Direction.EAST)) and (value := grid.get(position)):
        if value.isdigit():
            result = result + value

    return result

def get_contiguous_numerical_ranges(grid: Grid):
    contiguous_ranges = {}

    range_value = ''
    contiguous_range = ()
    previous_position = None

    for position, value in grid.items():
        # Was the last cell directly before this one?
        left_position = compute_new_position(position, Direction.WEST)
        if previous_position and previous_position != left_position:
            # The previous range has ended.
            if range_value:
                contiguous_ranges[contiguous_range] = range_value

            # The new range has begun
            range_value = ''
            contiguous_range = ()

        if value.isdigit():
            contiguous_range = (*contiguous_range, position)
            range_value += value
        else:
            # The previous range has ended.
            if range_value:
                contiguous_ranges[contiguous_range] = range_value

            # The new range has begun
            range_value = ''
            contiguous_range = ()


        previous_position = position

    # Add the last range in
    if range_value:
        contiguous_ranges[contiguous_range] = range_value

    return contiguous_ranges


Bounds = tuple[Position, Position, Position, Position]


def grid_bounds(grid: dict[Position, int]) -> Bounds:
    """Returns top left, top right, bottom left, bottom right"""
    xs = []
    ys = []
    for x, y in grid.keys():
        xs.append(x)
        ys.append(y)

    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)

    return (min_x, min_y), (max_x, min_y), (min_x, max_y), (max_x, max_y)


def point_within_bounds(position: Position, bounds: Bounds) -> bool:
    px, py = position
    tl_x, tl_y = bounds[0]
    br_x, br_y = bounds[3]
    within_x = tl_x <= px <= br_x
    within_y = tl_y <= py <= br_y
    return within_x and within_y


def points_within_bounds(grid, bounds: Bounds) -> list[Position]:
    return [
        position
        for position in grid.keys()
        if point_within_bounds(position, bounds)
    ]


def dict_grid_to_list(grid: dict) -> list[list[int]]:
    [tl_x, tl_y], _, _, [br_x, br_y] = grid_bounds(grid)
    return [
        [
            grid.get((x, y), None)
            for x in range(tl_x, br_x + 1)
        ]
        for y in range(tl_y, br_y + 1)
    ]


def all_grid_points(data: list[str]) -> Generator[Position, None, None]:
    for y, row in enumerate(data):
        for x, _ in enumerate(row):
            yield x, y