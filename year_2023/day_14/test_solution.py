from solution import Day

test_data = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 136


def test_run_step_2():
    assert Day(test_data).run_step_2() == 64
