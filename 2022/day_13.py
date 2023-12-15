import json
from functools import cmp_to_key


def parse_input(data: str):
    return [
        list(map(json.loads, pairs.split('\n')))
        for pairs in data.strip().split('\n\n')
    ]


def parse_input_2(data: str):
    return [
        json.loads(line)
        for line in data.strip().split('\n')
        if line
    ]


def compare(left: int | list, right: int | list) -> int:
    match left, right:
        case int(), int():
            return left - right

        case int(), list():
            return compare([left], right)

        case list(), int():
            return compare(left, [right])

        case list(), list():
            for res in map(compare, left, right):
                if res:
                    return res
            return compare(len(left), len(right))

        case _:
            raise Exception('Oh no!')


def run_step_1(data: str) -> int:
    packets = parse_input(data)
    return sum([
        index
        for index, packet in enumerate(packets, 1)
        if compare(*packet) < 0
    ])


def run_step_2(data: str) -> int:
    div_1 = [[2]]
    div_2 = [[6]]
    packets = parse_input_2(data) + [div_1] + [div_2]
    results = sorted(packets, key=cmp_to_key(compare))
    div_1_location = results.index(div_1) + 1
    div_2_location = results.index(div_2) + 1
    return div_1_location * div_2_location


if __name__ == "__main__":
    with open(f'data/day_13.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(f'Step 1: {result}')  # 5882

    result_2 = run_step_2(read_data)
    print(f'Step 2: {result_2}')  # 24948
