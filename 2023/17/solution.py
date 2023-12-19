import heapq
import os
from collections import deque
from functools import cache

from utils.grid import Position, Direction, compute_new_position


class Grid:
    def __init__(self, data):
        self.data = data
        self.grid_width, self.grid_height = len(self.data[0]) - 1, len(self.data) - 1

    @cache
    def calculate_next_options(
            self,
            position: Position,
            previous_direction: Direction,
            same_direction_count: int,
            minimum_steps: int,
            maximum_steps: int,
    ) -> set[Direction] | None:
        # Where can we go from here?
        x, y = position

        if same_direction_count < minimum_steps and previous_direction != Direction.NONE:
            return {previous_direction}

        options = {
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        }

        if previous_direction == Direction.WEST:
            options.remove(Direction.EAST)
        elif previous_direction == Direction.EAST:
            options.remove(Direction.WEST)
        elif previous_direction == Direction.NORTH:
            options.remove(Direction.SOUTH)
        elif previous_direction == Direction.SOUTH:
            options.remove(Direction.NORTH)

        if x == 0:
            options.discard(Direction.WEST)
        if y == 0:
            options.discard(Direction.NORTH)

        if same_direction_count >= maximum_steps:
            options.discard(previous_direction)

        return options


class Day:
    def __init__(self, data: str):
        self.data: list[list[int]] = [
            list(map(int, row))
            for row in data.splitlines()
        ]
        self.grid = Grid(self.data)

    def find_path(self, minimum_steps, maximum_steps) -> int:
        heap = [
            # Current heat index
            # Current position
            # Current direction
            # Number of times moved in that direction
            # History, for debuggin
            (0, (0, 0), Direction.NONE, 0, [(0, 0)])
        ]
        loop_avoidance = set()
        while heap:
            cost, position, direction, same_steps, history = heapq.heappop(heap)

            # Have we reached the end?
            if position == (self.grid.grid_width, self.grid.grid_height) and same_steps >= minimum_steps:
                return cost

            # Avoid spinning around in circles forever
            loop_avoidance_key = (position, direction, same_steps)
            if loop_avoidance_key in loop_avoidance:
                continue

            loop_avoidance.add(loop_avoidance_key)

            # Now figure out where we can go next
            options = self.grid.calculate_next_options(
                position,
                direction,
                same_steps,
                minimum_steps,
                maximum_steps,
            )
            for next_direction in options:
                next_x, next_y = compute_new_position(position, next_direction)

                try:
                    assert next_x >= 0
                    assert next_y >= 0
                    next_cost = self.data[next_y][next_x]
                except (IndexError, AssertionError):
                    # print(f'Failed to move {next_direction} to {next_x},{next_y}: {history}')
                    continue

                next_step_count = 1
                if direction == next_direction:
                    if same_steps < maximum_steps:
                        next_step_count = same_steps + 1

                heapq.heappush(heap, (
                    cost + next_cost,
                    (next_x, next_y),
                    next_direction,
                    next_step_count,
                    history + [(next_x, next_y)]
                ))

    def run_step_1(self) -> int:
        # 755
        return self.find_path(1, 3)

    def run_step_2(self) -> int:
        # 881
        return self.find_path(4, 10)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
