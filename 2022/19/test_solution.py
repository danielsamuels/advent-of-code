import pytest

from solution import Day

test_data = """
Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 33


@pytest.mark.parametrize('blueprint, expectation', zip(test_data.splitlines(), [9, 24]))
def test_step_1_individually(blueprint, expectation):
    assert Day(blueprint).run_step_1() == expectation


def test_run_step_2():
    assert Day(test_data).run_step_2() == 56 * 62
