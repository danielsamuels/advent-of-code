import copy
import enum
import itertools
from collections import defaultdict
from typing import Generator

from tqdm import trange, tqdm

from utils.grid import print_grid

row_options = [list(map(int, "{:b}".format(n).rjust(7 ,'0'))) for n in range(128)]


class RockType(enum.Enum):
    HORIZONTAL = [(0, 0), (1, 0), (2, 0), (3, 0)]
    PLUS = [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)]
    BACKWARDS_L = [(2, 0), (2, 1), (0, 2), (1, 2), (2, 2)]
    VERTICAL = [(0, 0), (0, 1), (0, 2), (0, 3)]
    SQUARE = [(0, 0), (1, 0), (0, 1), (1, 1)]


ROCK_TYPES = [
    RockType.HORIZONTAL,
    RockType.PLUS,
    RockType.BACKWARDS_L,
    RockType.VERTICAL,
    RockType.SQUARE,
]

step_history = {}

class Rock:
    x: int = 0
    y: int = 0

    def __init__(self, rock_type: RockType, world):
        self.type = rock_type
        self._points = rock_type.value
        self.world = world

        # 2D grid
        self.grid = defaultdict(lambda: defaultdict(bool))
        for x, y in self._points:
            self.grid[y][x] = True

        self.height = len(self.grid)
        self.width = max(len(row) for row in self.grid.values())

    def set_position(self, x: int, y: int):
        self.x = x
        self.y = y

    @property
    def points(self):
        # Where is this rock in space?
        # Assume that (x, y) is the top left corner
        return [
            (x + self.x, y + self.y)
            for y, row in self.grid.items()
            for x, col in row.items()
            if col
        ]

    def _translate_position(self, diff: tuple[int, int]) -> bool:
        dx, dy = diff
        target_positions = [(x + dx, y + dy) for x, y in self.points]
        in_wall = any(x > 6 or x < 0 for x, _ in target_positions)
        if in_wall:
            return False

        collisions = any(
            self.world.grid[y][x] != 0
            for x, y in target_positions
        )
        if collisions:
            return False

        self.x += dx
        self.y += dy
        return True

    def move_right(self) -> bool:
        # Is it possible to move right?
        # - Is there anything on the grid in the target positions?
        # - Is there a wall to our right?
        return self._translate_position((1, 0))

    def move_left(self) -> bool:
        return self._translate_position((-1, 0))

    def move_down(self) -> bool:
        return self._translate_position((0, 1))


class Day:
    def __init__(self, data: str, *, debug_level: int = 0):
        self.augment_height = 0
        self.augment_iteration = 0

        self.debug_level = debug_level

        self._steps = list(data)
        self.steps = self._step_generator()
        self.rocks = []
        self.rock = self._rock_generator()

        # Initialise a grid that is
        # 7 units wide and 100 units tall
        self.grid = []
        # for row in range(10):
        #     self.grid.append([0] * 7)
        self.grid.append([2] * 7)

    def _step_generator(self) -> Generator[str, None, None]:
        yield from itertools.cycle(enumerate(self._steps))

    def _rock_generator(self) -> Generator[Rock, None, None]:
        for rock_type in itertools.cycle(ROCK_TYPES):
            yield Rock(rock_type, self)

    def new_rock(self):
        # The rock should be 2 units away from the left wall
        # and the bottom edge 3 units above the highest rock
        rock = next(self.rock)

        # Ensure we have enough buffer at the top of the grid
        #
        # [0000000] - Top of grid
        # [0000000] - is space for
        # [0000000] - the new rock
        # [       ] - buffer
        # [       ] - buffer
        # [       ] - buffer
        # [   @   ] - Occupied space
        # [-------] - Floor
        rows_in_use = self.structure_height()
        free_rows = len(self.grid) - rows_in_use
        rows_to_insert = (rock.height + 3) - free_rows
        for _ in range(rows_to_insert):
            self.grid.insert(0, [0] * 7)

        placement_row = free_rows + max(rows_to_insert, 0) - 3 - rock.height
        # if placement_row < rock.height:
        #     # Add some new rows to the grid
        #     for _ in range(rock.height):
        #
        #     placement_row = rock.height + 1

        rock.set_position(2, placement_row)
        return rock

    def structure_height(self) -> int:
        # Get the index of the highest row with something in it
        return len(self.grid) - self.highest_occupied_row + self.augment_height

    @property
    def highest_occupied_row(self):
        return min([
            index
            for index, row in enumerate(self.grid)
            if any(column != 0 for column in row)
        ])

    def place_rock_on_grid(self, rock: Rock):
        self.rocks.append(rock)
        for x, y in rock.points:
            self.grid[y][x] = 1

        if self.debug_level > 0:
            print('Saving rock position. New grid is:')
            print_grid(self.grid)
            print('')

    def print_prospective_grid(self, rock: Rock):
        grid_copy = copy.deepcopy(self.grid)
        for x, y in rock.points:
            grid_copy[y][x] = 1

        if self.debug_level > 0:
            print_grid(grid_copy)
            print('')

    def process_steps(self, iteration: int, rock: Rock):
        # Without placing the rock on the grid, process the steps
        # When the steps are complete, add the rock to the grid
        # This avoids computing collisions without itself
        place_rock = True

        for step_index, step in self.steps:
            # Before continuing, check to see if we've been here before.
            cache_key = (self.column_depths(), rock.type, step_index)
            if cache_key in step_history:
                # How long ago did we last see this item?
                # What was the height of the stack at that time?
                prev_iteration, prev_height = step_history[cache_key]
                curr_height = self.structure_height()
                self.augment_height += curr_height - prev_height
                self.augment_iteration += prev_iteration - iteration
                place_rock = False
                break
            else:
                step_history[cache_key] = (iteration, self.structure_height())

            success = False
            if step == '>':
                success = rock.move_right()
            elif step == '<':
                success = rock.move_left()

            if self.debug_level >= 3:
                print(f'Move {step}: {success}')
                self.print_prospective_grid(rock)

            success = rock.move_down()
            if self.debug_level >= 3:
                print(f'Move down: {success}')
                self.print_prospective_grid(rock)

            if not success:
                if self.debug_level >= 2:
                    print('Rock has come to rest')
                break

        if place_rock:
            self.place_rock_on_grid(rock)

    def column_depths(self) -> tuple[int]:
        # What is the distance from the top of the column to the bottom?
        top_row = self.highest_occupied_row
        distances = [0 for _ in range(7)]
        for row in range(top_row, len(self.grid)):
            for col, val in enumerate(self.grid[row]):
                if distances[col] == 0 and val != 0:
                    distances[col] = row - top_row + 1

        return tuple(distances)

    @property
    def in_cycle(self):
        # For each row of the grid, calculate a value
        if len(self.grid) < 80:
            return False

        encoded_grid = ''.join([
            str(row_options.index(row))
            for row in self.grid
            if row not in [
                [0] * 7,
                [2] * 7,
            ]
        ])
        # Do the last 30 items match something we've done before?
        # size = 30
        # start_row = self.highest_occupied_row + 4
        # end_row = start_row + size
        search, space = encoded_grid[4:34], encoded_grid[34:]
        return search in space

    def run_process(self, iterations: int) -> int:
        fn = range if self.debug_level != 0 else trange

        base_iteration = 0
        with tqdm(total=iterations) as progress:
            while (iteration := base_iteration + self.augment_iteration) < iterations:
                progress.update(iteration)
                rock = self.new_rock()

                if self.debug_level > 0:
                    print('New rock, who dis?')
                    self.print_prospective_grid(rock)

                self.process_steps(iteration, rock)
                base_iteration += 1

            return self.structure_height() - 1


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    # day = Day(read_data)
    #
    # result = day.run_process(2022)
    # print(f'Step 1: {result}')

    # result_2 = day.run_process(1_000_000_000_000)
    # print(f'Step 2: {result_2}')
