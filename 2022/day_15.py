import itertools
import re
from collections import defaultdict

from tqdm import tqdm, trange

from utils.grid import compute_new_position, bridge_points, Position, manhattan_distance
from utils.ranges import merge_ranges


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
        print('Parsing input')
        sensors = defaultdict(tuple)
        beacons = defaultdict(bool)

        lines = re.findall(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)', data)
        for line in lines:
            sx, sy, bx, by = map(int, line)
            sensors[sx, sy] = (bx, by)
            beacons[bx, by] = True

        return sensors, beacons

    def calculate_distances(self):
        print('Calculating distances')
        distances = defaultdict(lambda: dict())
        for sensor, beacon in itertools.product(self.sensors, self.beacons):
            distances[sensor][beacon] = manhattan_distance(sensor, beacon)
        return distances

    def calculate_invalid_position_ranges(self) -> dict[int, list[range]]:
        print(f'Calculating invalid position ranges')

        ranges = defaultdict(list)
        for sensor, beacon in tqdm(self.sensors.items()):
            distance = self.distances[sensor][beacon]
            for line in range(-distance, distance):
                new_position = compute_new_position(sensor, (0, line))
                leftmost_point = compute_new_position(new_position, (-(distance - abs(line)), 0))
                rightmost_point = compute_new_position(new_position, (distance - abs(line), 0))
                ranges[new_position[1]].append(range(leftmost_point[0], rightmost_point[0] + 1))

        return ranges

    def calculate_invalid_positions(self, target_row: int, target_range: list[int] = None) -> set[int]:
        positions = []

        for sensor, closest_beacon in tqdm(self.sensors.items()):
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
        invalid_positions = self.calculate_invalid_position_ranges()
        print('Searching for position')
        for row in trange(cap):
            row_ranges = merge_ranges(invalid_positions[row])
            if len(row_ranges) == 1:
                # Does this range encapsulate the entire range we're interested in?
                row_range = row_ranges.pop()
                if row_range[0] <= 0 and row_range[-1] >= cap:
                    # The entire row is covered, move on
                    continue

            # missing = [
            #     col
            #     for col in range(cap)
            #     if (
            #         col not in [x for x, y in self.sensors.keys() if y == row]
            #         and col not in [x for x, y in self.beacons.keys() if y == row]
            #         and not any([
            #             col in invalid_range
            #             for invalid_range in invalid_positions[row]
            #         ])
            #     )
            # ]
            #

            row_sensors = set(x for x, y in self.sensors.keys() if y == row)
            row_beacons = set(x for x, y in self.beacons.keys() if y == row)
            row_invalids = set(itertools.chain(*invalid_positions[row]))
            missing = set(range(cap)) - row_invalids - row_sensors - row_beacons

            # print(f'=> Sensors={row_sensors}, Beacons={row_beacons}, Invalid Pos={invalid_positions[row]}, Invalid Set={row_invalids}')

            if missing:
                return missing.pop() * 4_000_000 + row

        raise Exception('Unable to find gap :(')


if __name__ == "__main__":
    with open(f'data/day_15.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    # result = day.run_step_1(2_000_000)
    # print(f'Step 1: {result}')

    result_2 = day.run_step_2(4_000_000)
    print(f'Step 2: {result_2}')
