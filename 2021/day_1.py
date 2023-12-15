class Day:
    def __init__(self, data: str):
        self.data = list(map(int, data.splitlines()))

    def run_step_1(self) -> int:
        last_value = None
        increases = 0
        for value in self.data:
            if last_value is None:
                last_value = value
                continue

            if value > last_value:
                increases += 1

            last_value = value

        return increases


    def run_step_2(self) -> int:
        # Sliding window slices of the range
        windows = [
            self.data[i:i+3]
            for i in range(len(self.data) - 2)
        ]

        last_value = None
        increases = 0
        for window in windows:
            value = sum(window)
            if last_value is None:
                last_value = value
                continue

            if value > last_value:
                increases += 1

            last_value = value

        return increases


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')