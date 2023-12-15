import itertools

import pytest

from year_2022.day_11 import run_step_1, parse_input, available_directions, all_available_directions, Direction, \
    node_index, run_step_2

test_data = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
""".strip()


def test_parse_input():
    heightmap, starting_point, target_point = parse_input(test_data)
    assert heightmap == [
        [0, 0, 1, 16, 15, 14, 13, 12],
        [0, 1, 2, 17, 24, 23, 23, 11],
        [0, 2, 2, 18, 25, 25, 23, 10],
        [0, 2, 2, 19, 20, 21, 22, 9],
        [0, 1, 3, 4, 5, 6, 7, 8],
    ]
    assert starting_point == (0, 0)
    assert target_point == (5, 2)


def test_run_step_1():
    assert run_step_1(test_data) == 31


@pytest.mark.parametrize('location, expectation', [
    [(0, 0), {Direction.EAST, Direction.SOUTH}],
    [(1, 0), {Direction.WEST, Direction.EAST, Direction.SOUTH}],
    [(2, 0), {Direction.WEST, Direction.SOUTH}],

    [(0, 1), {Direction.EAST, Direction.NORTH}],
    [(1, 1), {Direction.WEST, Direction.EAST, Direction.NORTH, Direction.SOUTH}],
    [(2, 1), {Direction.WEST, Direction.NORTH}],

    [(0, 2), {Direction.EAST, Direction.NORTH}],
    [(1, 2), {Direction.WEST, Direction.NORTH}],
    [(2, 2), {Direction.WEST, Direction.NORTH}],
])
def test_available_directions(location, expectation):
    layout = 'abc\nbcd\nedg'
    heightmap, _, _ = parse_input(layout)
    output = available_directions(heightmap, location)
    assert output == expectation


@pytest.mark.parametrize('position, expectation', list(
    zip(
        list(tuple(reversed(i)) for i in itertools.product(range(4), range(4))),
        range(16),
    )
))
def test_node_index(position, expectation):
    heightmap = [list(range(4))] * 4
    assert node_index(heightmap, position) == expectation


def test_run_step_2():
    assert run_step_2(test_data) == 29
