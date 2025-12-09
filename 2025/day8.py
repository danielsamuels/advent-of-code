from collections import defaultdict
import functools
import itertools
from operator import itemgetter
import operator
from pprint import pprint
from typing import ItemsView, Literal, Sequence, cast
from aocd import data, submit

from utils.grid import Position3D, euclidean_distance

test_data = """
162,817,812
57,618,57
906,360,560
592,479,940
352,342,300
466,668,158
542,29,236
431,825,988
739,650,466
52,470,668
216,146,977
819,987,18
117,168,530
805,96,715
346,949,466
970,615,88
941,993,340
862,61,35
984,92,344
425,690,689
""".strip()

TESTING = False
if TESTING:
    data = test_data
    iteration_limit = 10
else:
    iteration_limit = 1000

type PositionsWithDistance = tuple[Position3D, Position3D, float]


def calculate(part: Literal["a"] | Literal["b"] = "a") -> None:
    result = 0
    positions: list[Position3D] = [
        cast(Position3D, tuple(map(int, p)))
        for row in data.splitlines()
        if (p := row.split(","))
    ]

    distances: list[PositionsWithDistance] = sorted(
        [
            (p, q, euclidean_distance(p, q))
            for p, q in itertools.combinations(positions, 2)
        ],
        key=itemgetter(2),
    )

    # [
    #   [(a, b, c), (d, e, f)],
    #   [(g, h, i), (j, k, l)]
    # ]
    # => (a, b, c) is connected to (d, e, f)
    # => (g, h, i) is connected to (j, k, l)
    # circuits: list[set[Position3D]] = [{p} for p in positions]

    circuits = {p: i for i, p in enumerate(positions)}

    def circuit_length(circuit: int) -> int:
        result = len([v for v in circuits.values() if v == circuit])
        assert result > 0
        return result

    def num_circuits() -> int:
        return len(set(circuits.values()))

    def sorted_circuits() -> list[tuple[int, list[Position3D]]]:
        formed_circuits: dict[int, list[Position3D]] = defaultdict(list)
        for k, v in circuits.items():
            formed_circuits[v].append(k)

        return sorted(
            formed_circuits.items(),
            key=lambda c: len(c[1]),
            reverse=True,
        )

    def size_of_top_circuits(n: int) -> int:
        circuits = sorted_circuits()[:n]
        return functools.reduce(operator.mul, [len(v) for _, v in circuits])

    def change_circuit_for_all_members(current: int, target: int):
        # Change the circuit for all positions currently in `current` to be in `target`
        for position, circuit in circuits.items():
            if circuit == current:
                circuits[position] = target

    count = 0
    while distances:
        count += 1
        pqd = distances.pop(0)
        p, q, d = pqd
        cp, cq = circuits[p], circuits[q]
        cq_len = circuit_length(cq)
        cp_len = circuit_length(cp)

        print(
            f"\nIteration {count}: Looking at {p=} (circuit={cp}, len={cp_len}) and {q=} (circuit={cq}, len={cq_len})"
        )

        if cp == cq:
            print(f"=> BOTH in circuit {cp}, nothing to do")
        else:

            if cq_len > cp_len:
                print(f"=> Q len > P len, moving all members of {cp=} into {cq}")
                change_circuit_for_all_members(cp, cq)
            else:
                print(f"=> P len >= Q len, moving all members of {cq=} into {cp}")
                change_circuit_for_all_members(cq, cp)

        # Do we have what we need to determine the answer?
        if part == "a" and count == iteration_limit:
            result = size_of_top_circuits(3)
            break

        if part == "b" and num_circuits() == 1:
            result = p[0] * q[0]
            print(f"P2 is complete with {p[0]} and {q[0]} giving {result=}")
            break

    print(f"{result=}")
    if not TESTING:
        submit(result, part=part)

    # submit(p2_result, part='b')


def main():
    calculate("a")
    calculate("b")


if __name__ == "__main__":
    main()
