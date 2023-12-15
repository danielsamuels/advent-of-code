import operator

import pytest

from year_2022.day_11 import run_step_1, process_input, Monkey, run_round, run_step_2

test_data = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
""".strip()


def test_process_input():
    output, _, _ = process_input(test_data)
    expectation: list[Monkey] = [
        {
            'items': [79, 98],
            'operation': ['*', '19'],
            'divisible_by': 23,
            'if_true': 2,
            'if_false': 3,
        },
        {
            'items': [54, 65, 75, 74],
            'operation': ['+', '6'],
            'divisible_by': 19,
            'if_true': 2,
            'if_false': 0,
        },
        {
            'items': [79, 60, 97],
            'operation': ['*', 'old'],
            'divisible_by': 13,
            'if_true': 1,
            'if_false': 3,
        },
        {
            'items': [74],
            'operation': ['+', '3'],
            'divisible_by': 17,
            'if_true': 0,
            'if_false': 1,
        },
    ]
    assert output == expectation


@pytest.mark.parametrize('round_count, expectation', [
    [1, [
        [20, 23, 27, 26],
        [2080, 25, 167, 207, 401, 1046],
        [],
        [],
    ]],
    [2, [
        [695, 10, 71, 135, 350],
        [43, 49, 58, 55, 362],
        [],
        [],
    ]],
    [3, [
        [16, 18, 21, 20, 122],
        [1468, 22, 150, 286, 739],
        [],
        [],
    ]],
    [4, [
        [491, 9, 52, 97, 248, 34],
        [39, 45, 43, 258],
        [],
        [],
    ]],
    [5, [
        [15, 17, 16, 88, 1037],
        [20, 110, 205, 524, 72],
        [],
        [],
    ]],
])
def test_run_round(round_count, expectation):
    monkeys, inspections, _ = process_input(test_data)
    for _ in range(round_count):
        monkeys, inspections = run_round(monkeys, inspections)
    items = list(map(operator.itemgetter('items'), monkeys))
    assert items == expectation


def test_run_step_1():
    assert run_step_1(test_data) == 10605


@pytest.mark.parametrize('rounds, expectation', [
    [1, [2, 4, 3, 6]],
    [20, [99, 97, 8, 103]],
    [1000, [5204, 4792, 199, 5192]],
])
def test_inspections(rounds, expectation):
    monkeys, inspections, divisible_by_product = process_input(test_data)
    for _ in range(rounds):
        monkeys, inspections = run_round(monkeys, inspections, reduce_worry=divisible_by_product)

    assert inspections == expectation


def test_run_step_2():
    assert run_step_2(test_data) == 2713310158
