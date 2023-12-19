from utils.grid import Direction, compute_new_position, flood_fill
from utils.polygon import Polygon

directions = {
    'U': Direction.NORTH,
    'D': Direction.SOUTH,
    'L': Direction.WEST,
    'R': Direction.EAST,
    '0': Direction.EAST,
    '1': Direction.SOUTH,
    '2': Direction.WEST,
    '3': Direction.NORTH,
}


class Day:
    def __init__(self, data: str):
        self.data = [
            row.split()
            for row in data.splitlines()
        ]

    def run_step_1(self) -> int:
        position = (0, 0)
        grid = dict()

        for movement, meters, colour in self.data:
            for _ in range(int(meters)):
                position = compute_new_position(position, directions[movement])
                grid[position] = colour

        # 58550
        return flood_fill(grid)

    def run_step_2(self) -> int:
        # Decode the values
        position = (0, 0)
        vertices = [position]
        perimeter = 0

        for _, _, hex_value in self.data:
            meters = int(hex_value[2:7], 16)
            direction = directions[hex_value[7]]

            position = compute_new_position(position, direction, meters)
            vertices.append(position)
            perimeter += meters

        # 47452118468566
        polygon = Polygon(vertices)
        shoelace = polygon.shoelace()
        return polygon.picks(shoelace, perimeter)


if __name__ == '__main__':
    from aocd import data

    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
