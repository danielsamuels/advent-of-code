import operator
from aocd import data, submit

directions = {
    "L": operator.sub,
    "R": operator.add,
}


def main():
    position = 50
    p1_count = 0
    p2_count = 0

    for instruction in data.splitlines():
        direction: str = instruction[0]
        amount: int = int(instruction[1:])
        fn = directions[direction]

        for x in range(amount):
            position = fn(position, 1) % 100
            if position == 0:
                p2_count += 1

        if position % 100 == 0:
            p1_count += 1

    submit(p1_count, part="a")
    submit(p2_count, part="b")


if __name__ == "__main__":
    main()
