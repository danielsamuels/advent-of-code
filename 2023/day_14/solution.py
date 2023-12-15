import operator
from functools import cache

from utils.data import get_data
from utils.grid import parse_grid, Direction

Grid = tuple[tuple[tuple[int, int], str]]


@cache
def perform_cycle(new_grid: Grid, grid_width: int, grid_height: int):
    new_grid = shift_rocks(new_grid, Direction.NORTH, grid_width, grid_height)
    new_grid = shift_rocks(new_grid, Direction.WEST, grid_width, grid_height)
    new_grid = shift_rocks(new_grid, Direction.SOUTH, grid_width, grid_height)
    new_grid = shift_rocks(new_grid, Direction.EAST, grid_width, grid_height)
    return new_grid


@cache
def shift_rocks(grid: Grid, direction: Direction, grid_width: int, grid_height: int) -> Grid:
    new_grid = dict(grid)

    locations = new_grid.keys()
    if direction == Direction.NORTH:
        locations = sorted(locations, key=operator.itemgetter(1, 0))
    elif direction == Direction.SOUTH:
        locations = sorted(locations, key=operator.itemgetter(1, 0), reverse=True)
    elif direction == Direction.EAST:
        locations = sorted(locations, key=operator.itemgetter(0, 1), reverse=True)
    elif direction == Direction.WEST:
        locations = sorted(locations, key=operator.itemgetter(0, 1))

    for location in locations:
        thing = new_grid[location]
        if thing != 'O':
            continue

        new_location = location
        xs = ys = None

        if direction == Direction.NORTH:
            ys = range(location[1] - 1, -1, -1)
            xs = [location[0]] * len(ys)

        elif direction == Direction.SOUTH:
            ys = range(location[1] + 1, grid_height)
            xs = [location[0]] * len(ys)

        elif direction == Direction.EAST:
            xs = range(location[0] + 1, grid_width)
            ys = [location[1]] * len(xs)

        elif direction == Direction.WEST:
            xs = range(location[0] - 1, -1, -1)
            ys = [location[1]] * len(xs)

        assert xs is not None
        assert ys is not None

        for x, y in zip(xs, ys):
            if new_grid.get((x, y)):
                break
            new_location = (x, y)

        # Going to move this up to there then.
        if new_location != location:
            # print(f'Moving {location} ({thing}) to {new_location}')
            del new_grid[location]
            new_grid[new_location] = thing

    return tuple(new_grid.items())


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.grid = parse_grid(self.data, {
            '#': '#',
            'O': 'O',
        }, ignore_dots=True)

        self.tuple_grid = tuple(
            (location, value)
            for location, value in self.grid.items()
        )

    def score_grid(self, grid: Grid):
        return sum([
            len(self.data) - location[1]
            for location, thing in grid
            if thing == 'O'
        ])

    def run_step_1(self) -> int:
        grid_width, grid_height = len(self.data[0]), len(self.data)
        new_grid = shift_rocks(self.tuple_grid, Direction.NORTH, grid_width, grid_height)

        # 112048
        return self.score_grid(new_grid)

    def run_step_2(self) -> int:
        new_grid = self.tuple_grid
        grid_width, grid_height = len(self.data[0]), len(self.data)

        for cycle in range(1_000):
            new_grid = perform_cycle(new_grid, grid_width, grid_height)

        # 105606
        return self.score_grid(new_grid)


if __name__ == "__main__":
    data = get_data(__file__)

    day = Day(data)
    print(f'Step 1: {day.run_step_1()}')
    print(f'Step 2: {day.run_step_2()}')
