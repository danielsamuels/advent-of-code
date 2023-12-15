from utils.grid import parse_grid, DROP, Direction, WALL, grid_bounds, Position, move, relative_points_occupied

BLIZZARDS = {
    '>': Direction.EAST,
    '<': Direction.WEST,
    '^': Direction.NORTH,
    'v': Direction.SOUTH,
}


class Day:
    starting_position = (1, 0)

    def __init__(self, data: str):
        self.grid = parse_grid(data, mapping={
            '.': DROP,
            '#': WALL,
            **BLIZZARDS
        })
        self.position: Position = self.starting_position
        _, _, _, [br_x, br_y] = grid_bounds(self.grid)
        self.destination: Position = (br_x - 1, br_y)

    def move(self):
        new_grid = {}
        # Put the walls into the new grid

        # Move the blizzards first
        for position, value in self.grid.items():
            if value == WALL:
                new_grid[position] = value

            if value in BLIZZARDS.values():
                next_position = move(self.grid, position, value)
                new_grid[next_position] = value

        # Look at what options are available for us to move into
        occupied = relative_points_occupied(new_grid, self.position, [
            Direction.NORTH,
            Direction.EAST,
            Direction.SOUTH,
            Direction.WEST,
        ] if self.position != self.starting_position else [
            Direction.SOUTH
        ])
        print(occupied)

    def run_step_1(self) -> int:
        minute = 0
        while self.position != self.destination:
            minute += 1
            self.move()
        return minute

    def run_step_2(self) -> int: ...


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    result = Day(read_data).run_step_1()
    print(f'Step 1: {result}')

    result_2 = Day(read_data).run_step_2()
    print(f'Step 2: {result_2}')
