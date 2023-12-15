class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def run_race(self, time, distance, hold_time) -> bool:
        return ((time - hold_time) * hold_time) > distance

    def run_races(self, races) -> int:
        result = 1

        for time, distance in races:
            result *= sum(self.run_race(time, distance, h) for h in range(time))

        return result

    def run_step_1(self) -> int:
        times = map(int, self.data[0].split(':')[1].split())
        distances = map(int, self.data[1].split(':')[1].split())
        return self.run_races(zip(times, distances))

    def run_step_2(self) -> int:
        time = int(''.join(self.data[0].split(':')[1].split()))
        distance = int(''.join(self.data[1].split(':')[1].split()))
        return self.run_races([(time, distance)])
