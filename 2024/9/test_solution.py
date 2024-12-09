from solution import Day

test_data = "2333133121414131402"


def test_run_step_1():
    assert Day(test_data).run_step_1() == 1928


def test_run_step_2():
    assert Day(test_data).run_step_2() == 2858
