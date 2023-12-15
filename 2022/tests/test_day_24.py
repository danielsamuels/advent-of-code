from year_2022.day_24 import Day

test_data = """
#.#####
#.....#
#>....#
#.....#
#...v.#
#.....#
#####.#
""".strip('\n')


def test_run_step_1():
    assert Day(test_data).run_step_1() == 18


def test_run_step_2():
    assert Day(test_data).run_step_2() == 0
