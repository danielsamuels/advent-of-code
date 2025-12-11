import enum
import itertools
from collections import defaultdict, deque
import math
from typing import Generator, TypeVar, Any, Collection, Literal, overload
from typing import Optional

Position = tuple[int, int]
Position3D = tuple[int, int, int]
Grid = dict[Position, str]

DROP = object()
WALL = object()
T = TypeVar("T")


# sqrt(tiles / 6) = edge length


class Direction(Position, enum.Enum):
    NONE = (0, 0)
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
    diff_x, diff_y = tuple(
        itertools.starmap(lambda a, b: b - a, zip([start_x, start_y], end))
    )

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

    return ((x, y) for x, y in [])


def bridge_str_points(start: str, end: str) -> Generator[Position, None, None]:
    input_points = (start, end)
    start, end = [tuple(map(int, point.split(","))) for point in input_points]
    return bridge_points(start, end)


def compute_new_position(
    start: Position, diff: Position, iterations: int = 1
) -> Position:
    start_x, start_y = start
    diff_x, diff_y = diff
    return start_x + (diff_x * iterations), start_y + (diff_y * iterations)


def move(grid: dict[Position, T], start: Position, direction: Direction) -> Position:
    # Move a point by diff, wrapping if necessary.
    # Assume a square grid.
    px, py = start
    tl, tr, bl, br = grid_bounds(grid)
    new_position = compute_new_position(start, direction)
    new_cell = grid.get(new_position)

    # Wrapping!
    if new_cell == WALL:
        if direction == Direction.NORTH:
            # Find the bottom of this column
            new_position = (px, bl[1])
        elif direction == Direction.EAST:
            # Find the left of this row
            new_position = (tl[0], py)
        elif direction == Direction.SOUTH:
            # Find the top of this column
            new_position = (px, tl[1])
        elif direction == Direction.WEST:
            # Find the right of this row
            new_position = (br[0], py)
        else:
            raise Exception(f"Unhandled direction: {direction}")

        return move(grid, new_position, direction)

    return new_position


def bridge_diff(start: Position, diff: Position) -> Generator[Position, None, None]:
    end = compute_new_position(start, diff)
    return bridge_points(start, end)


def manhattan_distance(point_a, point_b):
    # Calculate the manhattan distance
    [ax, ay], [bx, by] = point_a, point_b
    return abs(ax - bx) + abs(ay - by)


P = TypeVar("P", Position, Position3D)


def euclidean_distance(p: P, q: P) -> float:
    dimensions = len(p)

    # https://en.wikipedia.org/wiki/Euclidean_distance#Two_dimensions
    if dimensions == 2:
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)

    # https://en.wikipedia.org/wiki/Euclidean_distance#Higher_dimensions
    elif dimensions == 3:
        return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2 + (p[2] - q[2]) ** 2)

    raise ValueError(f"Invalid positions provided, wrong number for {dimensions=}")


def print_grid(grid: list[list[int]], *, populated_char=None, borders=True):
    if populated_char is None:
        populated_char = "#"

    print()
    for row in grid:
        middle = "".join(
            "." if col is None else populated_char if populated_char else col
            for col in row
        )
        if borders:
            print("|", middle, "|")
        else:
            print(middle)


def find_in_grid(
    grid: list[str],
    target: str,
    *,
    x_hint: int | None = None,
    y_hint: int | None = None,
    multiple: bool = False,
) -> Generator[Position, None, None]:
    for y, row in enumerate(grid):
        if y_hint is not None and y != y_hint:
            continue

        for x, cell in enumerate(row):
            if x_hint is not None and x != x_hint:
                continue

            if cell == target:
                yield x, y

                if not multiple:
                    return


def parse_grid(
    data: list | str,
    mapping: Optional[bool | dict[str, T]] = None,
    *,
    ignore_dots: bool = False,
    add_index: bool = False,
) -> dict[Position, Any]:
    """Take a string and turn it into a dict"""
    index = 0

    if mapping is None:
        mapping = {
            ".": DROP,
            "#": 1,
        }

    if isinstance(data, str):
        data = data.splitlines()

    grid = defaultdict(int)

    for y, row in enumerate(data):
        for x, value in enumerate(row):
            if value == "." and ignore_dots:
                continue

            if mapping is not False:
                value = mapping.get(value, 1)

            if value == DROP:
                continue

            if add_index:
                index += 1
                value = {
                    "index": index,
                    "value": value,
                }

            grid[(x, y)] = value

    return dict(grid)


def print_sparse_grid(grid: Grid):
    """Given a list of positions, plot them on a map, filling in any gaps"""
    print()

    *_, br = grid_bounds(grid)
    x_key_len = len(str(br[0]))
    y_key_len = len(str(br[1])) + 1

    str_grid = "\n".join(
        [
            str(row).rjust(y_key_len - 1).ljust(y_key_len)
            + "".join([grid.get((col, row), ".") for col in range(0, br[0] + 1)])
            for row in range(0, br[1] + 1)
        ]
    )

    x_number_strs = [str(i).rjust(x_key_len).ljust(x_key_len) for i in range(br[0] + 1)]

    # Output an x-key
    for row in range(x_key_len):
        print("".ljust(y_key_len) + "".join(num[row] for num in x_number_strs))

    print(str_grid)
    print()


def relative_points_occupied(
    grid: dict, position: Position, directions: list[Direction]
) -> list[bool]:
    return [
        grid.get(compute_new_position(position, direction), False)
        for direction in directions
    ]


def all_relative_point_occupation(
    grid: dict, position: Position
) -> dict[Direction, dict]:
    """From a given point, which directions are occupied?"""
    result = {}
    for direction in Direction:
        point = compute_new_position(position, direction)
        if point_val := grid.get(point):
            result[direction] = {"position": point, "value": point_val}

    return result


def cardinal_points(position) -> list[tuple[Direction, Position]]:
    return [
        (direction, compute_new_position(position, direction))
        for direction in [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ]
    ]


def cardinal_point_occupation(
    grid: Collection[Collection[Any]], position: Position
) -> dict[Direction, dict]:
    result = {}
    width, height = len(grid[0]), len(grid)

    for direction, position in cardinal_points(position):
        col, row = position
        if col < 0 or col >= width:
            continue
        if row < 0 or row >= height:
            continue

        if grid[row][col]:
            result[direction] = {
                "position": (col, row),
                "value": grid[row][col],
            }

    return result


def get_contiguous_value(grid: Grid, position: Position):
    """From a given position, find the start and end point of a string"""
    start_point = position
    result = grid.get(start_point)

    while (position := compute_new_position(position, Direction.WEST)) and (
        value := grid.get(position)
    ):
        if value.isdigit():
            result = value + result

    position = start_point
    while (position := compute_new_position(position, Direction.EAST)) and (
        value := grid.get(position)
    ):
        if value.isdigit():
            result = result + value

    return result


def get_contiguous_numerical_ranges(grid: Grid):
    contiguous_ranges = {}

    range_value = ""
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
            range_value = ""
            contiguous_range = ()

        if value.isdigit():
            contiguous_range = (*contiguous_range, position)
            range_value += value
        else:
            # The previous range has ended.
            if range_value:
                contiguous_ranges[contiguous_range] = range_value

            # The new range has begun
            range_value = ""
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
        position for position in grid.keys() if point_within_bounds(position, bounds)
    ]


def dict_grid_to_list(
    grid: dict, grid_width: int = None, grid_height: int = None
) -> list[list[Any]]:
    if grid_width and grid_height:
        tl_x, tl_y = (0, 0)
        br_x, br_y = (grid_width - 1, grid_height - 1)
    else:
        [tl_x, tl_y], _, _, [br_x, br_y] = grid_bounds(grid)
    return [
        [grid.get((x, y), None) for x in range(tl_x, br_x + 1)]
        for y in range(tl_y, br_y + 1)
    ]


def all_grid_points(data: list[str]) -> Generator[Position, None, None]:
    for y, row in enumerate(data):
        for x, _ in enumerate(row):
            yield x, y


def flood_fill(grid: dict | list):
    # Expand the grid by 1 in all directions
    if isinstance(grid, dict):
        grid = dict_grid_to_list(grid)

    width, height = len(grid[0]), len(grid)
    empty_row = [None] * width

    grid.insert(0, empty_row)
    grid.append(empty_row)
    for index, row in enumerate(grid):
        grid[index] = [None, *row, None]

    width, height = len(grid[0]), len(grid)

    # Start from (0, 0) and fill
    frontier = deque([(0, 0)])
    reached = {(0, 0)}

    while frontier:
        location = frontier.pop()
        points = cardinal_point_occupation(grid, location).values()
        for point in points:
            if point["position"] not in reached and not point["value"]:
                frontier.append(point["position"])
                reached.add(point["position"])

    # Subtract the flooded space from the overall grid,
    # leaving the filled area we care about behind
    return width * height - len(reached)


def rotate_direction(
    current_direction, rotation: Literal["cw"] | Literal["ccw"]
) -> Direction:
    if rotation == "cw":
        if current_direction == Direction.NORTH:
            return Direction.EAST
        elif current_direction == Direction.EAST:
            return Direction.SOUTH
        elif current_direction == Direction.SOUTH:
            return Direction.WEST
        elif current_direction == Direction.WEST:
            return Direction.NORTH
