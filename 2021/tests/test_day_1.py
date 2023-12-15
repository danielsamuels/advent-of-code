from year_2021.day_1 import Day

test_data = """
199
200
208
210
200
207
240
269
260
263
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 7


def test_run_step_2():
    assert Day(test_data).run_step_2() == 5