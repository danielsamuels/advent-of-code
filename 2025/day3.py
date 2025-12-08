# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "advent-of-code-data",
#     "tqdm",
# ]
# ///

from collections import deque
import itertools
from aocd import data, submit
from tqdm import tqdm

# data = """
# 987654321111111
# 811111111111119
# 234234234234278
# 818181911112111
# """.strip()

type QueueValue = list[tuple[int, int]]


def determine_next_value(
    # This is in the deque format: [(index, value), (index, value), ...]
    current_values: QueueValue,
    remaining_values: QueueValue,
    bank_length: int,
    target_length: int,
    excluded_values: list[int],
) -> QueueValue:
    if not remaining_values:
        return []

    current_index = current_values[-1][0] + 1 if current_values else 0

    # Remaining values: [7, 6, 5, 4]
    candidate_value = max([v for _, v in remaining_values if v not in excluded_values])

    needed = target_length - len(current_values)
    max_index = current_index + len(remaining_values) - needed

    candidates = [
        (i, v) for i, v in remaining_values if i <= max_index and v == candidate_value
    ]
    if not candidates:
        # This value is not viable, move on to another
        return determine_next_value(
            current_values,
            remaining_values,
            bank_length,
            target_length,
            [*excluded_values, candidate_value],
        )

    return candidates


def calculate(target_length: int) -> int:
    answers = []

    for line in data.splitlines():
        # To make life easier, convert all of the values into indexed ints now
        bank: QueueValue = list((i, int(v)) for i, v in enumerate(line))
        bank_length = len(bank)
        print(f"Working on {line} with {target_length=}")

        # Get the largest first number possible for a `target_length` digit number
        # There's no point in looking at any others
        start_values = determine_next_value([], bank, bank_length, target_length, [])
        # We might have multiple options here, e.g. for a bank of 987987987 with `target_length=2` we'd get [(0, 9), (3, 9), (6, 9)]
        # These are separate start points, so split them out into their own queues.
        options = deque([v] for v in start_values)
        candidates = set()

        while options:
            current = options.popleft()

            if len(current) == target_length:
                # There's nothing more to do with this one, turn it into an int and move on.
                candidate = int("".join(str(v) for i, v in current))
                candidates.add(candidate)
                continue

            current_index = current[-1][0]
            remaining_values = bank[current_index + 1 :]
            next_options = determine_next_value(
                current,
                remaining_values,
                bank_length,
                target_length,
                [],
            )
            for option in next_options:
                options.appendleft([*current, option])

        print(f"Answer {max(candidates)} from {len(candidates)} candidates")
        answers.append(max(candidates))

    return sum(answers)


def main() -> None:
    part_1 = calculate(2)
    print(f"{part_1=}")
    part_2 = calculate(12)
    print(f"{part_2=}")

    # submit(calculate(2), part="a")
    # submit(calculate(12), part="b")


if __name__ == "__main__":
    main()
