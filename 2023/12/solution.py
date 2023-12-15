import itertools
from functools import cache

storage = {}


@cache
def compute(row: str, row_index: int, groups: tuple, groups_index: int, block_length: int) -> int:
    storage_key = (row_index, groups_index, block_length)
    if stored_value := storage.get(storage_key):
        return stored_value

    # If we're at the end of the row...
    if len(row) == row_index:
        if groups_index == len(groups) and block_length == 0:
            # We're working on the last block, and we're out of space
            return 1

        if groups_index == len(groups) - 1 and groups[groups_index] == block_length:
            # We've reached the length we need
            return 1

        # Nothing more to do here
        return 0

    result = 0

    current_char = row[row_index]
    for char in ['.', '#']:
        if current_char in [char, '?']:
            if char == '.' and block_length == 0:
                result += compute(row, row_index + 1, groups, groups_index, 0)
            elif char == '.' and block_length > 0 and groups_index < len(groups) and groups[
                groups_index] == block_length:
                result += compute(row, row_index + 1, groups, groups_index + 1, 0)
            elif char == '#':
                result += compute(row, row_index + 1, groups, groups_index, block_length + 1)

    storage[storage_key] = result
    return result


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.records = self.parse_records()

    def parse_records(self):
        records = []
        for record in self.data:
            row, groups = record.split()
            groups = list(map(int, groups.split(',')))
            records.append((row, groups))

        return records

    @staticmethod
    def calculate_arrangements(row, groups):
        storage.clear()
        result = compute(row, 0, tuple(groups), 0, 0)
        assert result > 0
        return result

    def run_step_1(self) -> int:
        # 7490
        return sum(itertools.starmap(self.calculate_arrangements, self.records))

    def run_step_2(self) -> int:
        # Unfold the data
        expanded_data = [
            ('?'.join([k] * 5), v * 5)
            for k, v in self.records
        ]

        # 65607131946466
        return sum(itertools.starmap(self.calculate_arrangements, expanded_data))
