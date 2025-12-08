from collections import defaultdict
import functools
import itertools
import operator
import re
from aocd import data, submit


operator_mapping = {
    "*": operator.mul,
    "+": operator.add,
}


def part_1() -> None:
    lines = data.splitlines()
    problems = []
    # Structure: [{ "values": [1, 2, 3], "operator": mul }, {...}]

    for operator in lines[-1].split():
        problems.append(
            {
                "values": [],
                "operator": operator_mapping[operator],
            }
        )

    for line in lines[:-1]:
        for i, v in enumerate(line.split()):
            problems[i]["values"].append(int(v))

    result = sum(map(lambda p: functools.reduce(p["operator"], p["values"]), problems))
    print(f"{result=}")
    submit(result, part="a")


def part_2() -> None:
    lines = data.splitlines()
    problems = []
    # Structure: [{ "values": [1, 2, 3], "operator": mul }, {...}]

    current_problem = {"operator": None, "values": []}
    for column in range(len(lines[-1]) - 1, -1, -1):
        operator = lines[-1][column].strip()
        current_problem["operator"] = operator_mapping.get(
            operator,
            current_problem["operator"],
        )

        column_value = "".join(line[column] for line in lines[:-1]).strip()

        if column_value:
            current_problem["values"].append(int(column_value))

        if not column_value or column == 0:
            # Push the current value and operator into the list
            problems.append(current_problem)

            # Reset the current problem back to default
            current_problem = {"operator": None, "values": []}

    result = sum(map(lambda p: functools.reduce(p["operator"], p["values"]), problems))
    print(f"{result=}")
    submit(result, part="b")


def main() -> None:
    part_1()
    part_2()


if __name__ == "__main__":
    main()
