from solution import Day

test_data = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
""".strip()

test_data_step_2 = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 142


def test_run_step_2():
    assert Day(test_data_step_2).run_step_2() == 281
