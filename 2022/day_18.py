import itertools
from collections import defaultdict

from utils.dijkstra import Graph

DIRECTIONS = [
    (-1, 0, 0),
    (1, 0, 0),
    (0, -1, 0),
    (0, 1, 0),
    (0, 0, -1),
    (0, 0, 1),
]

class Day:
    def __init__(self, data: str):
        self.cubes = self.parse_input(data)

        x_vals = sorted(set(c[0] for c in self.cubes))
        self.x_range = min(x_vals), max(x_vals)
        y_vals = sorted(set(c[1] for c in self.cubes))
        self.y_range = min(y_vals), max(y_vals)
        z_vals = sorted(set(c[2] for c in self.cubes))
        self.z_range = min(z_vals), max(z_vals)

    def parse_input(self, data: str) -> list[tuple]:
        return [
            tuple(map(int, line.split(',')))
            for line in data.splitlines()
        ]

    def compute_unconnected_faces(self):
        return sum([
            (x + dx, y + dy, z + dz) not in self.cubes
            for x, y, z in self.cubes
            for dx, dy, dz in DIRECTIONS
        ])

    def compute_unconnected_sans_interior(self):
        combined = set(self.cubes) | self.interior_cubes()
        return sum([
            (x + dx, y + dy, z + dz) not in self.cubes
            for x, y, z in combined
            for dx, dy, dz in DIRECTIONS
        ])

    def compute_external_faces(self) -> int:
        # Build a 3d grid
        all_cubes = set(self.cubes) | self.interior_cubes()
        grid = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        for x, y, z in self.cubes:
            grid[z][y][x] = 1

        for z in range(self.z_range[0], self.z_range[1] + 1):
            column = [0]
            for y in range(self.y_range[0], self.y_range[1] + 1):
                for x in range(self.x_range[0], self.x_range[1] + 1):
                    print(grid[z])

        return 0

    def interior_cubes(self) -> set[tuple]:
        x_min, x_max = self.x_range
        y_min, y_max = self.y_range
        z_min, z_max = self.z_range

        # For each cube, is there a cube on:
        # - The same X-axis to the left and right
        # - The same Y-axis to the left and right
        # - The same Z-axis to the left and right
        surrounded_cubes = []
        all_coords = itertools.product(
            range(x_min, x_max + 1),
            range(y_min, y_max + 1),
            range(z_min, z_max + 1),
        )

        for x, y, z in all_coords:
            surroundings = [
                # X lt & gt
                [(n, y, z) for n in range(x_min, x)],
                [(n, y, z) for n in range(x + 1, x_max + 1)],
                # Y lt & gt
                [(x, n, z) for n in range(y_min, y)],
                [(x, n, z) for n in range(y + 1, y_max + 1)],
                # Z lt & gt
                [(x, y, n) for n in range(z_min, z)],
                [(x, y, n) for n in range(z + 1, z_max + 1)],
            ]
            surrounded = all([
                any(cube in self.cubes for cube in cubes)
                for cubes in surroundings
            ])
            if surrounded:
                surrounded_cubes.append((x, y, z))

        return set(surrounded_cubes)

    def run_step_1(self) -> int:
        return self.compute_unconnected_faces()

    def run_step_2(self) -> int:
        return self.compute_external_faces()


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    # 2029 is too low
    # 2067 is too high
    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
