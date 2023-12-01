class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def run_step_1(self) -> int: ...
    def run_step_2(self) -> int: ...


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
