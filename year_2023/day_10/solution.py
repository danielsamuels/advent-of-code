from utils.grid import parse_grid, Connection, find_in_grid, all_relative_point_occupation, Position, Direction, \
    compute_new_position, all_grid_points

MOVEMENTS = {
    # If we hit a connection, and we're travelling in a given direction,
    # where should we go next?
    # This allows us to account for bends in the pipes.
    (Connection.VERTICAL, Direction.NORTH): Direction.NORTH,
    (Connection.VERTICAL, Direction.SOUTH): Direction.SOUTH,
    (Connection.HORIZONTAL, Direction.EAST): Direction.EAST,
    (Connection.HORIZONTAL, Direction.WEST): Direction.WEST,

    (Connection.NORTHEAST, Direction.SOUTH): Direction.EAST,
    (Connection.NORTHEAST, Direction.WEST): Direction.NORTH,
    (Connection.NORTHWEST, Direction.EAST): Direction.NORTH,
    (Connection.NORTHWEST, Direction.SOUTH): Direction.WEST,

    (Connection.SOUTHEAST, Direction.NORTH): Direction.EAST,
    (Connection.SOUTHEAST, Direction.WEST): Direction.SOUTH,
    (Connection.SOUTHWEST, Direction.NORTH): Direction.WEST,
    (Connection.SOUTHWEST, Direction.EAST): Direction.SOUTH,
}


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.width, self.height = len(self.data[0]), len(self.data)

        self.mapping = {
            'S': Connection.START,
            '|': Connection.VERTICAL,
            '-': Connection.HORIZONTAL,
            'L': Connection.NORTHEAST,
            'J': Connection.NORTHWEST,
            '7': Connection.SOUTHWEST,
            'F': Connection.SOUTHEAST,
        }
        self.grid = parse_grid(data, self.mapping, ignore_dots=True)
        self.path = self.compute_path()

    def available_directions(self, position: Position):
        return [
            (direction, data)
            for direction, data in all_relative_point_occupation(self.grid, position).items()
            if direction in data['value'].value
        ]

    def compute_path(self):
        # Find the start, work out what type it is
        S = find_in_grid(self.data, 'S')
        S_dirs = [d[0] for d in self.available_directions(S)]

        path = [S]
        position = S
        direction = S_dirs[0]

        while True:
            position = compute_new_position(position, direction)
            symbol = self.grid[position]

            if symbol == Connection.START:
                break

            direction = MOVEMENTS[(symbol, direction)]

            if position == S:
                break

            path.append(position)

        return path

    def run_step_1(self) -> int:
        return len(self.path) // 2

    def count_intersections(self, position) -> int:
        # If odd, inner, if even, outside
        count = 0
        corners = [
            self.mapping['L'],
            self.mapping['7'],
        ]
        direction = Direction.SOUTHEAST

        while position := compute_new_position(position, direction):
            if position[0] > self.width or position[1] > self.height:
                break

            value = self.grid[position]
            if position in self.path and value not in corners:
                count += 1

        return count % 2 == 1

    def run_step_2(self) -> int:
        # For each point, go diagonally out and
        # see how many times we cross the path
        return sum([
            self.count_intersections(position)
            for position in all_grid_points(self.data)
            if position not in self.path
        ])


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)
    print(f'Step 1: {day.run_step_1()}')
    print(f'Step 2: {day.run_step_2()}')
