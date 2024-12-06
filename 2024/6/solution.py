from tqdm import tqdm

from utils.grid import parse_grid, DROP, Direction, cardinal_point_occupation, find_in_grid, rotate_direction, \
    all_grid_points


class Day:
    def __init__(self, data: str):
        self.grid = data.splitlines()

    def calculate(self) -> set:
        position = find_in_grid(self.grid, '^')
        visited_locations = set()
        direction = Direction.NORTH

        while True:
            visited_locations.add(position)

            directions = cardinal_point_occupation(self.grid, position)
            if direction not in directions:
                break
            next_position = directions[direction]
            if next_position['value'] in ['.', '^']:
                position = next_position['position']
                continue
            elif next_position['value'] == '#':
                direction = rotate_direction(direction, 'cw')

        return visited_locations

    def run_step_1(self) -> int:
        visited_locations = self.calculate()
        return len(visited_locations)

    def run_step_2(self) -> int:
        step_1_locations = self.calculate()

        viable_locations = set()
        start_position = find_in_grid(self.grid, '^')

        for x, y in tqdm(step_1_locations):
            if self.grid[y][x] in ['^', '#']:
                continue

            # Reset the data
            position = start_position
            visited_locations = []
            direction = Direction.NORTH

            while True:
                pos_dir = (position, direction)
                if pos_dir in visited_locations:
                    # We've been here before and are in a loop
                    viable_locations.add((x, y))
                    break

                visited_locations.append(pos_dir)

                directions = cardinal_point_occupation(self.grid, position)
                if direction not in directions:
                    break

                next_position = directions[direction]
                if next_position["position"] == (x, y):
                    next_position['value'] = '#'

                if next_position['value'] in ['.', '^']:
                    position = next_position['position']
                    continue
                elif next_position['value'] == '#':
                    direction = rotate_direction(direction, 'cw')

        return len(viable_locations)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
