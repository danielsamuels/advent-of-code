Values = list[tuple[int, int]]


class Day:
    inputs: Values = []

    def __init__(self, data: str, step: int = 1):
        # Give every value a unique value
        if step == 1:
            self.inputs = [
                (index, int(line))
                for index, line in enumerate(data.splitlines())
            ]
        else:
            decryption_key = 811589153
            self.inputs = [
                (index, int(line) * decryption_key)
                for index, line in enumerate(data.splitlines())
            ]

    def process_inputs(self, values: Values = None) -> Values:
        if values is None:
            values = self.inputs

        values = values.copy()
        values_len = len(self.inputs)

        for item in self.inputs:
            index, command = item
            # Calculate the new position
            current_index = values.index(item)
            new_index = (current_index + command) % (values_len - 1)
            # Remove the item from the list
            values.remove(item)
            # Add the item at the new position
            values.insert(new_index, item)

        return values

    @staticmethod
    def calculate_score(arrangement: Values) -> int:
        # Get the value of the number at positions 1000, 2000 and 3000 after the 0.
        zero_item = next(item for item in arrangement if item[1] == 0)
        zero_position = arrangement.index(zero_item)
        restructured_list = arrangement[zero_position:] + arrangement[:zero_position]

        one_thou = 1000 % len(restructured_list)
        two_thou = 2000 % len(restructured_list)
        three_thou = 3000 % len(restructured_list)
        results = [restructured_list[one_thou], restructured_list[two_thou], restructured_list[three_thou]]
        return sum([r[1] for r in results])

    def run_step_1(self) -> int:
        new_arrangement = self.process_inputs(self.inputs)
        return self.calculate_score(new_arrangement)

    def run_step_2(self) -> int:
        inputs = self.inputs
        for _ in range(10):
            inputs = self.process_inputs(inputs)
        return self.calculate_score(inputs)


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read().strip()

    result = Day(read_data).run_step_1()
    print(f'Step 1: {result}')

    result_2 = Day(read_data, step=2).run_step_2()
    print(f'Step 2: {result_2}')
