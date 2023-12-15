from functools import reduce
from pprint import pprint
from typing import TypedDict, Callable


class Monkey(TypedDict):
    items: list[int]
    operation: list[str]
    divisible_by: int
    if_true: int  # Target monkey
    if_false: int  # Target monkey


def run_operation(old: int, operator: str, adjuster: str) -> int:
    new = 0
    match [operator, adjuster]:
        case ['*', 'old']:
            return old * old
        case ['+', 'old']:
            return old + old
        case ['*', num]:
            return old * int(num)
        case ['+', num]:
            return old + int(num)
        case _:
            raise Exception('Unhandled operation: %s %s', operator, adjuster)


def process_input(data: str) -> tuple[list[Monkey], list[int], int]:
    monkeys = data.split('\n\n')
    monkeys_out = []
    total_div_by = 1

    num_monkeys = len(monkeys)

    for monkey_input in monkeys:
        monkey_output: Monkey = dict()
        for descriptor in monkey_input.split('\n')[1:]:
            match descriptor.strip().split():
                case ['Starting', 'items:', *items]:
                    monkey_output['items'] = list(map(lambda i: int(i.replace(',', '')), items))
                case ['Operation:', 'new', '=', 'old', operator, adjuster]:
                    monkey_output['operation'] = [operator, adjuster]
                case ['Test:', 'divisible', 'by', num]:
                    monkey_output['divisible_by'] = int(num)
                    total_div_by *= int(num)
                case ['If', boolean, 'throw', 'to', 'monkey', num]:
                    if boolean == 'true:':
                        monkey_output['if_true'] = int(num)
                    else:
                        monkey_output['if_false'] = int(num)

        monkeys_out.append(monkey_output)

    return monkeys_out, [0] * num_monkeys, total_div_by


def run_round(monkeys: list[Monkey], inspections: list[int], reduce_worry: int = 3) -> tuple[list[Monkey], list[int]]:
    monkeys = monkeys.copy()
    for index, monkey in enumerate(monkeys):
        inspections[index] += len(monkey['items'])

        while monkey['items']:
            item = monkey['items'].pop(0)
            worry_level = run_operation(item, *monkey['operation'])

            if reduce_worry == 3:
                worry_level = worry_level // 3
            else:
                worry_level = worry_level % reduce_worry

            if worry_level % monkey['divisible_by'] == 0:
                # Throw the item to another monkey
                monkeys[monkey['if_true']]['items'].append(worry_level)
            else:
                monkeys[monkey['if_false']]['items'].append(worry_level)

    return monkeys, inspections


def run_step_1(data: str) -> int:
    monkeys, inspections, _ = process_input(data)

    for round_num in range(20):
        monkeys, inspections = run_round(monkeys, inspections)

    most_active_monkeys = sorted(inspections, reverse=True)[:2]
    return most_active_monkeys[0] * most_active_monkeys[1]


def run_step_2(data: str) -> int:
    monkeys, inspections, divisible_by_product = process_input(data)

    for _ in range(10_000):
        monkeys, inspections = run_round(monkeys, inspections, reduce_worry=divisible_by_product)

    most_active_monkeys = sorted(inspections, reverse=True)[:2]
    return most_active_monkeys[0] * most_active_monkeys[1]


if __name__ == "__main__":
    with open(f'data/day_11.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)
