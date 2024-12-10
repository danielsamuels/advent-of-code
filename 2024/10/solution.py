import heapq

from utils.grid import find_in_grid, Position, cardinal_point_occupation


class Day:
    def __init__(self, data: str):
        self.data: list[list[int]] = [list(map(int, line)) for line in data.splitlines()]
        self.zeroes: list[Position] = list(find_in_grid(self.data, 0, multiple=True))

    def calculate(self, position: Position, part=1) -> int:
        positions_reached = set()
        # Where can we go from here?
        heap = [
            # Length, position, current value
            (0, [position])
        ]
        while heap:
            value, positions = heapq.heappop(heap)
            points = cardinal_point_occupation(self.data, positions[-1])
            for location in points.values():
                if value == 8 and location["value"] == 9:
                    if part == 1:
                        positions_reached.add(location["position"])
                    else:
                        positions_reached.add((*positions, location["position"]))

                    continue

                if location["value"] == value + 1:
                    heapq.heappush(heap, (
                        location["value"],
                        [*positions, location["position"]],
                    ))

        return len(positions_reached)

    def run_step_1(self) -> int:
        return sum(self.calculate(start_pos) for start_pos in self.zeroes)

    def run_step_2(self) -> int:
        return sum(self.calculate(start_pos, part=2) for start_pos in self.zeroes)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
