import itertools
import operator
import string
from functools import reduce

all_items = string.ascii_lowercase + string.ascii_uppercase


def detect_duplicates(*args: tuple[str]) -> list[str]:
    items = [set(item) for item in args]
    return list(reduce(operator.and_, items))


def score_item(item: str) -> int:
    return all_items.index(item) + 1


def score_duplicates(items: list[str]) -> list[int]:
    return map(score_item, items)


def run_step_1(data: str) -> int:
    """
    Each row represents a backback, there are two equally sized compartments.
    The items are uniquely determined by the characters [a-zA-Z].
    Get the items which appear in both compartments.
    For each item, a score is given for it's position in the character range.
    Sum the scores of the duplicates.
    """
    backpacks = [[pack[0:len(pack) // 2], pack[len(pack) // 2:]] for pack in data.split('\n')]
    backpack_duplicates = itertools.starmap(detect_duplicates, backpacks)
    backpack_scores = map(score_duplicates, backpack_duplicates)
    backpack_sums = map(sum, backpack_scores)

    return sum(backpack_sums)

def run_step_2(data: str) -> int:
    backpacks = data.split('\n')
    # Group the backpacks into groups of 3
    num_groups = len(backpacks) // 3
    groups = [
        [backpacks[n * 3], backpacks[(n * 3) + 1], backpacks[(n * 3) + 2]]
        for n in range(num_groups)
    ]
    common_items = itertools.starmap(detect_duplicates, groups)
    common_scores = map(score_item, [item[0] for item in common_items])

    return sum(common_scores)


if __name__ == "__main__":
    with open('data/day_3.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)