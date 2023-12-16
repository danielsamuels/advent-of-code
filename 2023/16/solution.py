from collections import deque
from functools import cache

from utils.grid import parse_grid, Connection, Position, Direction, compute_new_position


class Grid:
    def __init__(self, data: list[str], start_position: Position, start_direction: Direction):
        self.data = data
        self.start_position = start_position

        self.grid_width, self.grid_height = len(self.data[0]) - 1, len(self.data) - 1
        self.grid = parse_grid(self.data, {
            '|': Connection.VERTICAL,
            '-': Connection.HORIZONTAL,
            '/': Connection.SOUTHEAST,
            '\\': Connection.SOUTHWEST,
        }, ignore_dots=True)
        self.visited_cells = set()

        self.queue = deque()
        self.queue.append((start_position, start_direction))

    @cache
    def calculate_next_step(self, current_position: Position, direction: Direction):
        x, y = current_position
        if len(self.visited_cells) > 0:
            if x < 0 or x > self.grid_width:
                return
            if y < 0 or y > self.grid_height:
                return

        # print(current_position, direction)

        if current_position != self.start_position:
            self.visited_cells.add(current_position)

        next_position = compute_new_position(current_position, direction)
        next_value = self.grid.get(next_position)

        if next_value is None:
            # Nothing here, carry on in this direction
            return self.queue.append((next_position, direction))

        # Take care of the passthrough beams first
        if direction in [Direction.NORTH, Direction.SOUTH] and next_value == Connection.VERTICAL:
            return self.queue.append((next_position, direction))
        if direction in [Direction.EAST, Direction.WEST] and next_value == Connection.HORIZONTAL:
            return self.queue.append((next_position, direction))

        # Then take a look at the change of directions
        changes = {
            Direction.NORTH: {Connection.SOUTHEAST: Direction.EAST, Connection.SOUTHWEST: Direction.WEST},
            Direction.EAST: {Connection.SOUTHEAST: Direction.NORTH, Connection.SOUTHWEST: Direction.SOUTH},
            Direction.SOUTH: {Connection.SOUTHEAST: Direction.WEST, Connection.SOUTHWEST: Direction.EAST},
            Direction.WEST: {Connection.SOUTHEAST: Direction.SOUTH, Connection.SOUTHWEST: Direction.NORTH},
        }

        if next_direction := changes[direction].get(next_value):
            return self.queue.append((next_position, next_direction))

        # Then look at the splts
        if direction in [Direction.EAST, Direction.WEST] and next_value == Connection.VERTICAL:
            # We're splitting the beam!
            self.queue.append((next_position, Direction.NORTH))
            self.queue.append((next_position, Direction.SOUTH))
            return
        if direction in [Direction.NORTH, Direction.SOUTH] and next_value == Connection.HORIZONTAL:
            # We're splitting the beam!
            self.queue.append((next_position, Direction.WEST))
            self.queue.append((next_position, Direction.EAST))
            return

        assert next_direction

        return self.queue.append((next_position, next_direction))

    def exhaust_queue(self):
        while self.queue:
            self.calculate_next_step(*self.queue.popleft())

        return len(self.visited_cells)


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.grid_width, self.grid_height = len(self.data[0]) - 1, len(self.data) - 1

    def run_step_1(self) -> int:
        start_position = (-1, 0)
        grid = Grid(self.data, start_position, Direction.EAST)
        return grid.exhaust_queue()

    def outside_edges(self):
        for x in range(self.grid_width):
            # Top row, looking down
            yield (x, -1), Direction.SOUTH
            # Bottom row, looking up
            yield (x, self.grid_height + 1), Direction.NORTH

        for y in range(self.grid_height):
            # Left side, going right
            yield (-1, y), Direction.EAST
            # Right side, going left
            yield (self.grid_width + 1, y), Direction.WEST

    def run_step_2(self) -> int:
        return max([
            Grid(self.data, position, direction).exhaust_queue()
            for position, direction in self.outside_edges()
        ])


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 1: {Day(data).run_step_2()}')
