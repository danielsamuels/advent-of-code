import enum
import itertools

Position = tuple[int, int]
Sand = set[Position]
Walls = set[Position]


class Status(enum.Enum):
    OK = enum.auto()
    BLOCKED = enum.auto()
    OUT_OF_BOUNDS = enum.auto()


def bridge_points(input_points: tuple[str, str]) -> Walls:
    [start_x, start_y], end = [tuple(map(int, point.split(','))) for point in input_points]
    diff_x, diff_y = tuple(itertools.starmap(lambda a, b: b - a, zip([start_x, start_y], end)))
    output_points = set()

    if diff_x != 0:
        step = int(diff_x / abs(diff_x))
        r = list(range(start_x, start_x + diff_x + step, step))
        for new_x in r:
            output_points.add((new_x, start_y))
    elif diff_y != 0:
        step = int(diff_y / abs(diff_y))
        r = list(range(start_y, start_y + diff_y + step, step))
        for new_y in r:
            output_points.add((start_x, new_y))

    return output_points


def process_input(data: str, step: int = 1) -> Walls:
    walls = set([
        p
        for wall in data.split('\n')
        for points in itertools.pairwise(wall.split(' -> '))
        for p in bridge_points(points)
    ])

    # Step 2: Add another wall
    if step == 2:
        bottom = max(y for x, y in walls) + 2
        for p in bridge_points((f'-1000,{bottom}', f'1000,{bottom}')):
            walls.add(p)

    return walls


def in_bounds(walls, position) -> bool:
    left = min(x for x, y in walls)
    bottom = max(y for x, y in walls)
    right = max(x for x, y in walls)

    x, y = position

    return left <= x <= right and y <= bottom


def attempt_move(position, movement, in_bounds_fn, sand, walls) -> tuple[Status, Position]:
    # Can we move down and to the left?
    pos_x, pos_y = position
    mov_x, mov_y = movement
    target_position = (pos_x + mov_x, pos_y + mov_y)
    if target_position in sand or target_position in walls:
        # Unable to move
        return Status.BLOCKED, (pos_x, pos_y)

    # Would this take us off the edge of the world?
    if not in_bounds_fn(walls, target_position):
        return Status.OUT_OF_BOUNDS, position

    return Status.OK, target_position


def available_moves(position, in_bounds_fn, sand, walls):
    moves = [
        attempt_move(position, (0, 1), in_bounds_fn, sand, walls),
        attempt_move(position, (-1, 1), in_bounds_fn, sand, walls),
        attempt_move(position, (1, 1), in_bounds_fn, sand, walls),
    ]
    return [
        (status, position)
        for status, position in moves
        if status != Status.BLOCKED
    ]


def plot_sand_unit_path(in_bounds_fn, sand: Sand, walls: Walls):
    start = position = (500, 0)
    while moves := available_moves(position, in_bounds_fn, sand, walls):
        position_changed = False
        for move in moves:
            if move[0] == Status.OK:
                position = move[1]
                position_changed = True
                break

        # The only option is out of bounds
        if not position_changed:
            return

    if position != start:
        return position


def run_step_1(data: str) -> int:
    data = process_input(data)
    sand = set()
    while position := plot_sand_unit_path(in_bounds, sand, data):
        sand.add(position)
    return len(sand)


def run_step_2(data: str) -> int:
    data = process_input(data, 2)
    sand = set()
    while position := plot_sand_unit_path(lambda x, y: True, sand, data):
        sand.add(position)
    return len(sand) + 1


if __name__ == "__main__":
    with open(f'data/day_14.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)
