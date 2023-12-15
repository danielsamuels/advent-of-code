from solution import Day

test_data = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 114


def test_run_step_2():
    assert Day(test_data).run_step_2() == 2
