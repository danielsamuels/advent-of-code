# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "advent-of-code-data",
#     "tqdm",
# ]
# ///

import itertools
from aocd import data, submit
from tqdm import tqdm

# data = """
# 987654321111111
# 811111111111119
# 234234234234278
# 818181911112111
# """.strip()


def main() -> None:
    p1_result = 0
    p2_result = 0

    for bank in tqdm(data.splitlines()):
        p1_result += max(int("".join(p)) for p in itertools.combinations(bank, 2))

    print(f"P1 result: {p1_result}")
    submit(p1_result, part="a")


if __name__ == "__main__":
    main()
