import re
from aocd import data, submit


def main():
    p1_result = 0
    p2_result = 0

    ranges = data.split(",")
    ranges = [range(*map(int, r.split("-"))) for r in ranges]
    for values in ranges:
        for value in values:
            if re.fullmatch(r"\b(\d+)\1\b", str(value)):
                p1_result += value

            if re.fullmatch(r"\b(\d+)\1+\b", str(value)):
                p2_result += value

    submit(p1_result, part="a")
    submit(p2_result, part="b")
    return p1_result


if __name__ == "__main__":
    main()
