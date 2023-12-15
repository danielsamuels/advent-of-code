from solution import Day

test_data = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 405


def test_run_step_2():
    assert Day(test_data).run_step_2() == 400
