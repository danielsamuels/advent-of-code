from aocd import data, submit

from utils.ranges import merge_ranges

# data = """
# 3-5
# 10-14
# 16-20
# 12-18
# 9-21

# 1
# 5
# 8
# 11
# 17
# 32
# """.strip()


def setup() -> tuple[list[range], list[int]]:
    fresh_ranges, ingredients = data.split("\n\n")
    fresh_ranges = fresh_ranges.splitlines()
    ingredients = list(map(int, ingredients.splitlines()))

    ranges = []
    for str_range in fresh_ranges:
        minval, maxval = map(int, str_range.split("-"))
        # Be sure to make it inclusive at the top
        ranges.append(range(minval, maxval + 1))

    return ranges, ingredients


def part1() -> None:
    ranges, ingredients = setup()

    fresh_ingredients = [
        ingredient for ingredient in ingredients if any(ingredient in r for r in ranges)
    ]
    result = len(fresh_ingredients)

    print(f"{result=}")
    submit(result, part="a")


def part2() -> None:
    ranges, _ = setup()
    merged_ranges = merge_ranges(ranges)
    result = sum(len(r) for r in merged_ranges)
    print(f"{result=}")
    submit(result, part="b")


def main() -> None:
    part1()
    part2()


if __name__ == "__main__":
    main()
