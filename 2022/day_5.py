import re
from collections import deque


def process_layout(layout: str) -> list[deque[str]]:
    # Split the string into rows
    rows = layout.split('\n')
    # Determine the number of columns (from the last row)
    column_count = max([int(n) for n in rows.pop().split(' ') if n])
    # Split each row into 3 character columns, space-separated
    # 0-4, 4-8, 8-12 etc
    indexes = list(range(1, column_count * 4, 4))

    row_crates = [
        [row[n] for n in indexes]
        for row in reversed(rows)
    ]
    # Transform the rows into columns
    column_crates = [
        deque(filter(lambda x: x != ' ', [row[column] for row in row_crates]))
        for column in range(column_count)
    ]
    return column_crates


def process_steps(steps: str) -> list[dict[str, int]]:
    steps = [
        re.match(r'move (?P<count>\d+) from (?P<from>\d+) to (?P<to>\d+)', row)
        for row in steps.split('\n')
        if row
    ]
    return [
        {
            'count': int(step.group('count')),
            'from': int(step.group('from')),
            'to': int(step.group('to')),
        }
        for step in steps
    ]


def process_input(data: str) -> tuple[list[deque[str]], list[dict[str, int]]]:
    # Split the input into the current layout and the steps
    layout, steps = data.split('\n\n')
    layout = process_layout(layout)
    steps = process_steps(steps)
    return layout, steps


def perform_steps(layout: list[deque[str]], steps: list[dict[str, int]]) -> list[deque[str]]:
    for step in steps:
        for tick in range(step['count']):
            # Pop off `from` and push on `to`. Instructions are 1-indexed
            source_stack = layout[step['from'] - 1]
            target_stack = layout[step['to'] - 1]

            # Move an item from the source to the target
            item_moving = source_stack.pop()
            target_stack.append(item_moving)

    return layout


def perform_steps_grouped(layout: list[deque[str]], steps: list[dict[str, int]]) -> list[deque[str]]:
    for step in steps:
        # Pop off `from` and push on `to`. Instructions are 1-indexed
        source_stack = layout[step['from'] - 1]
        target_stack = layout[step['to'] - 1]

        # Remove the target number of items
        temp_stack = deque([])
        for tick in range(step['count']):
            # Move an item from the source to the target
            item_moving = source_stack.pop()
            temp_stack.append(item_moving)

        # Move all the items from the temp stack into the new stack
        # Retain the original ordering
        while temp_stack:
            target_stack.append(temp_stack.pop())

    return layout


def calculate_result(layout: list[deque[str]]) -> str:
    return ''.join(c.pop() for c in layout)


def run_step_1(data: str) -> str:
    layout, steps = process_input(data)
    new_layout = perform_steps(layout, steps)
    return calculate_result(new_layout)


def run_step_2(data: str) -> str:
    layout, steps = process_input(data)
    new_layout = perform_steps_grouped(layout, steps)
    return calculate_result(new_layout)


if __name__ == "__main__":
    with open(f'data/day_5.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)