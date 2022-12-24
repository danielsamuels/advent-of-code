import enum
import itertools
import re
from typing import Generator

from utils.grid import Direction, compute_new_position, find_in_grid


def _identifier():
    yield from range(100_000)


identifier = _identifier()


class Day:
    def __init__(self, data: str):
        grid, instructions = data.split('\n\n')
        grid = [list(row) for row in grid.splitlines()]
        # Replace positions with IDs
        self.grid = [
            [next(identifier) if cell == '.' else cell for cell in row]
            for row in grid
        ]

        self.instructions = map(
            lambda i: int(i) if i not in ['L', 'R'] else i,
            [s for s in re.split(r'([LR])', instructions) if s != '']
        )
        self.direction = Direction.EAST
        self.position = (next(i for i, v in enumerate(self.grid[0]) if v != ' '), 0)

        self.x_cycles = [
            [column for column in row if column != ' ']
            for row in self.grid
        ]
        self.y_cycles = [
            [
                row[column] for row in self.grid
                if len(row) > column and row[column] != ' '
            ]
            for column in range(max(len(row) for row in self.grid))
        ]

    @property
    def position_id(self):
        px, py = self.position
        return self.grid[py][px]

    def rotate(self, rotation: str) -> None:
        directions = [Direction.WEST, Direction.NORTH, Direction.EAST, Direction.SOUTH]
        rotations = {'L': -1, 'R': 1}
        d_index = directions.index(self.direction) + rotations[rotation]
        d_index %= len(directions)
        new_direction = directions[d_index]
        print(f'Rotating {rotation}, changing from {self.direction.name} to {new_direction.name}')
        self.direction = new_direction

    def move(self, steps: int):
        print(f'Moving {steps} steps from {self.position} in direction {self.direction.name}')

        # If wanted to move X steps in Y direction, where do we _actually_ end up?
        # This is taking into account walls, wrapping etc.

        if self.direction in [Direction.WEST, Direction.EAST]:
            cycle = self.x_cycles[self.position[1]]
            fixed_x, fixed_y = False, True
        else:
            cycle = self.y_cycles[self.position[0]]
            fixed_x, fixed_y = True, False

        if self.direction in [Direction.WEST, Direction.NORTH]:
            cycle = cycle[::-1]

        position_index = cycle.index(self.position_id) + 1
        restructured = itertools.cycle(cycle[position_index:] + cycle[:position_index])

        new_position_index = self.position_id
        for step in range(steps):
            pos = next(restructured)
            if pos == '#':
                print('> Hit a wall')
                break
            new_position_index = pos

        # Find this identifier within the overall grid
        x_hint, y_hint = None, None
        if fixed_x:
            x_hint = self.position[0]
        if fixed_y:
            y_hint = self.position[1]

        new_position = find_in_grid(self.grid, new_position_index, x_hint, y_hint)
        print(f'Ended up at {new_position}')
        self.position = new_position

    def run_step_1(self) -> int:
        print()

        for instruction in self.instructions:
            if instruction in ['L', 'R']:
                self.rotate(instruction)
            else:
                self.move(instruction)

        facing_scores = {
            Direction.EAST: 0,
            Direction.SOUTH: 1,
            Direction.WEST: 2,
            Direction.NORTH: 3,
        }
        print(f'Final position: {self.position}, facing {self.direction.name}')
        return sum([
            1000 * (self.position[1] + 1),
            4 * (self.position[0] + 1),
            facing_scores[self.direction],
        ])

    def run_step_2(self) -> int:
        ...


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    # 26324 is too low
    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
