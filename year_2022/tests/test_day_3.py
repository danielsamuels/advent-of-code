from year_2022.day_3 import run_step_1, run_step_2

test_data = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


def test_run_step_1():
    result = run_step_1(test_data.strip())
    assert result == 157


def test_run_step_2():
    result = run_step_2(test_data.strip())
    assert result == 70
