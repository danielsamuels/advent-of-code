from collections import defaultdict
from functools import cmp_to_key


class Day:
    def __init__(self, data: str):
        self.rules = defaultdict(set)

        rules, updates = data.split("\n\n")
        for rule in rules.splitlines():
            before, after = rule.split("|")
            self.rules[before].add(after)

        self.updates: list[list[str]] = [u.split(',') for u in updates.splitlines()]

    def sort_update(self, update: list[str]) -> int:
        def rule_based_sort(a: str, b: str) -> int:
            # Does a have a requirement for b to be in front?
            if b in self.rules[a]:
                return -1
            if a in self.rules[b]:
                return 1
            return 0

        sorted_update = sorted(update, key=cmp_to_key(rule_based_sort))
        return int(sorted_update[len(update) // 2])

    def calculate(self, update: list[str], part_2=False) -> int:
        # Is this update correctly sorted?
        for index, item in enumerate(update):
            # Get the items that follow
            remainder = set(update[index + 1:])

            if remainder - self.rules[item]:
                if part_2:
                    return self.sort_update(update)
                return False

        # Return the middle number in the list
        if part_2:
            return False

        return int(update[len(update) // 2])

    def run_step_1(self) -> int:
        return sum(self.calculate(item) for item in self.updates)

    def run_step_2(self) -> int:
        return sum(self.calculate(item, part_2=True) for item in self.updates)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
