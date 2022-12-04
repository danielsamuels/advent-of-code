from year_2022.day_4 import run_step_1, run_step_2

test_data = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()


def test_day_4_step_1():
    output = run_step_1(test_data)
    assert output == 2


def test_day_4_step_2():
    output = run_step_2(test_data)
    assert output == 4
