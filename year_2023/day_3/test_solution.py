from solution import Day

test_data = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 4361


def test_run_step_2():
    assert Day(test_data).run_step_2() == 467835
