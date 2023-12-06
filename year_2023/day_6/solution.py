from math import floor

from tqdm import trange


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def run_race(self, time, distance, hold_time) -> bool:
        return ((time - hold_time) * hold_time) > distance

    def run_races(self, races) -> int:
        result = 1

        for time, distance in races:
            result *= sum(self.run_race(time, distance, h) for h in range(distance))

        return result

    def run_step_1(self) -> int:
        times = map(int, self.data[0].split(':')[1].split())
        distances = map(int, self.data[1].split(':')[1].split())
        return self.run_races(zip(times, distances))

    def run_step_2(self) -> int:
        time = int(''.join(self.data[0].split(':')[1].split()))
        distance = int(''.join(self.data[1].split(':')[1].split()))
        distances = range(distance)

        parts = 100_000_000
        part_indexes = {
            part: floor(len(distances) * (part / parts))
            for part in range(parts)
        }

        first_part = last_part = None

        prev_value = False
        for part, index in part_indexes.items():
            result = self.run_race(time, distance, distances[index])

            if not prev_value and result:
                first_part = part

            if prev_value and not result:
                last_part = part
                break

            prev_value = result

        return sum(
            self.run_race(time, distance, h)
            for h in trange(part_indexes[first_part - 1], part_indexes[last_part + 1])
        )


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
