from solution import Day

test_data = "125 17"


def test_run_step_1():
    assert Day(test_data).run_step_1() == 55312


def test_run_step_2():
    assert Day(test_data).run_step_2() == 0
