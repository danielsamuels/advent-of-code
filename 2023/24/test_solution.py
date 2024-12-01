from solution import Day

test_data = """
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 0


def test_run_step_2():
    assert Day(test_data).run_step_2() == 0
