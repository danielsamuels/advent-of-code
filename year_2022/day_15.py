import itertools
import re
from collections import defaultdict

from utils.grid import compute_new_position, bridge_points


class Day:
    sensors: dict
    beacons: dict
    distances: dict
    invalid_positions: dict

    def __init__(self, data):
        self.sensors, self.beacons = self.parse_input(data)
        print(f'{len(self.sensors)} sensors, {len(self.beacons)} beacons')
        self.distances = self.calculate_distances()

    @staticmethod
    def parse_input(data: str) -> tuple[dict, dict]:
        sensors = defaultdict(tuple)
        beacons = defaultdict(bool)

        lines = re.findall(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', data)
        for line in lines:
            sx, sy, bx, by = map(int, line)
            sensors[sx, sy] = (bx, by)
            beacons[bx, by] = True

        return sensors, beacons

    def calculate_distances(self):
        distances = defaultdict(lambda: dict())
        for sensor, beacon in itertools.product(self.sensors, self.beacons):
            # Calculate the manhattan distance
            diff_x, diff_y = abs(sensor[0] - beacon[0]), abs(sensor[1] - beacon[1])
            distances[sensor][beacon] = diff_x + diff_y

        return distances

    def calculate_invalid_positions(self, target_row: int, target_range: list[int] = None) -> set[int]:
        positions = []

        for sensor, closest_beacon in self.sensors.items():
            print(f' - Sensor {sensor}')
            distance_to_beacon = self.distances[sensor][closest_beacon]

            for scanline in range(distance_to_beacon + 1):
                for y in [scanline, -scanline]:
                    up_from_sensor = compute_new_position(sensor, (0, y))

                    if up_from_sensor[1] != target_row:
                        continue

                    print(f'- Processing {up_from_sensor}')
                    leftmost_point = compute_new_position(up_from_sensor, (-distance_to_beacon + scanline, 0))
                    rightmost_point = compute_new_position(up_from_sensor, (distance_to_beacon - scanline, 0))

                    if leftmost_point == rightmost_point:
                        row_positions = [leftmost_point]
                    else:
                        row_positions = list(bridge_points(leftmost_point, rightmost_point))

                    print(f'  - {len(row_positions)} points')
                    for px, py in row_positions:
                        if (px, py) in self.sensors or (px, py) in self.beacons:
                            continue

                        if target_range is not None:
                            range_low, range_high = target_range
                            if px < range_low or px > range_high:
                                continue

                        positions.append(px)

        return set(positions)

    def run_step_1(self, row: int) -> int:
        invalid_positions = self.calculate_invalid_positions(row)
        return len(invalid_positions)

    def run_step_2(self, cap: int) -> int:
        for row in range(cap):
            print(f'Calculating invalid positions for row {row}')
            invalid_positions = self.calculate_invalid_positions(row, [0, cap])
            # Missing items
            missing = set(range(cap)) - invalid_positions
            print(f'{len(missing)} items missing from row {row}')
            for column in missing:
                pos = (column, row)
                if pos not in self.sensors and pos not in self.beacons:
                    return column * 4_000_000 + row

        return 0


if __name__ == "__main__":
    with open(f'data/day_15.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    # result = day.run_step_1(2_000_000)
    # print(f'Step 1: {result}')

    result_2 = day.run_step_2(4_000_000)
    print(f'Step 2: {result_2}')
