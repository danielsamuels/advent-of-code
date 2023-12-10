class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def run_step_1(self) -> int:
        return 0

    def run_step_2(self) -> int:
        return 0


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)
    print(f'Step 1: {day.run_step_1()}')
    print(f'Step 2: {day.run_step_2()}')
