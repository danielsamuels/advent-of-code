import pytest

from solution import Day

test_data = [
    (
        """
.....
.S-7.
.|.|.
.L-J.
.....
""".strip(), 4
    ),
    (
        """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
""".strip(), 8
    ),
    (
        """
7-F7-
.FJ|7
SJLL7
|F--J
LJ.LJ
""".strip(), 8
    ),

]

def test_run_step_1_simple():
    data = """
.....
.S-7.
.|.|.
.L-J.
.....
""".strip()

    # (1, 1) -> (1, 2) -> (1, 3) -> (2, 3) -> (3, 3)
    # (1, 1) -> (2, 1) -> (3, 1) -> (3, 2) -> (3, 3)
    assert Day(data).run_step_1() == 4


@pytest.mark.parametrize('layout, expected_distance', test_data)
def test_run_step_1(layout, expected_distance):
    assert Day(layout).run_step_1() == expected_distance


step_2_data_1 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
""".strip()

step_2_data_2 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
""".strip()


@pytest.mark.parametrize('layout, expected_value', [
    (step_2_data_1, 4),
    # (step_2_data_2, 10),
])
def test_run_step_2(layout, expected_value):
    assert Day(layout).run_step_2() == expected_value
