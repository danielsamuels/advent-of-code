class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def run_step_1(self) -> int:
        return 0

    def run_step_2(self) -> int:
        return 0


if __name__ == "__main__":
    from aocd import get_data
    import pathlib

    parts = pathlib.Path().absolute().parts
    day = int(next(p[4:] for p in parts if p.startswith('day_')))
    year = int(next(p[5:] for p in parts if p.startswith('year_')))
    data = get_data(year=year, day=day)

    day = Day(data)
    print(f'Step 1: {day.run_step_1()}')
    print(f'Step 2: {day.run_step_2()}')
