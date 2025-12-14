import functools
import itertools
from operator import xor

from aocd import data, submit

test_data = """
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
""".strip()

TESTING = False
if TESTING:
    data = test_data


def convert_buttons(button_strs: list[str]) -> list[int]:
    # Turn '(1,3)' into 5
    return [
        sum(1 << int(value) for value in button_str[1:-1].split(","))
        for button_str in button_strs
    ]


def calculate_button_presses_for_machine(requirements, buttons) -> int:
    for r in range(1, len(buttons) + 1):
        for button_set in itertools.combinations(buttons, r=r):
            status = functools.reduce(xor, button_set)
            if status == requirements:
                return len(button_set)

    return 0


def part_1() -> int:
    machines = []
    for line in data.splitlines():
        requirements, *button_strs, joltages = line.split(" ")
        requirements = int(
            requirements[1:-1].replace("#", "1").replace(".", "0")[::-1], 2
        )

        # Turn (1, 2) into 0110 (turning those specific bits on, 1st and 2nd)
        buttons = convert_buttons(button_strs)
        assert len(buttons) == len(button_strs)
        joltages = [list(map(int, j)) for j in joltages[1:-1].split(",")]

        machine = (requirements, buttons, joltages)
        print(f"{machine=}")
        machines.append(machine)

    return sum(
        [
            calculate_button_presses_for_machine(requirements, buttons)
            for requirements, buttons, _ in machines
        ]
    )


if __name__ == "__main__":
    p1_result = part_1()
    print(f"{p1_result=}")
    if not TESTING:
        submit(p1_result, part="a")

    # submit(p2_result, part='b')
