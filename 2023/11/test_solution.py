import pytest

from solution import Day

test_data = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
""".strip()


def test_run_step_1():
    day = Day(test_data)
    assert sorted(set(day.locations)) == sorted({
        (4, 0), (9, 1), (0, 2), (8, 5), (1, 6), (12, 7), (9, 10), (0, 11), (5, 11)
    })
    assert day.run_step_1() == 374


@pytest.mark.parametrize('expansion_amount, expected_result', [
    (2, 374),
    (10, 1030),
    (100, 8410),
])
def test_run_step_2(expansion_amount, expected_result):
    assert Day(test_data).run_step_2() == expected_result
