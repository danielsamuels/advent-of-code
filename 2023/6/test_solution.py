from solution import Day

test_data = """
Time:      7  15   30
Distance:  9  40  200
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 288


def test_run_step_2():
    assert Day(test_data).run_step_2() == 71503
