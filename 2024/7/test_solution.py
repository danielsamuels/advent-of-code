from solution import Day

test_data = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 3749


def test_run_step_2():
    assert Day(test_data).run_step_2() == 11387
