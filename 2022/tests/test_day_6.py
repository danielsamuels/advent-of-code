import pytest

from year_2022.day_6 import run_step_1, run_step_2


@pytest.mark.parametrize('buffer, expectation', [
    ['mjqjpqmgbljsphdztnvjfqwrcgsmlb', 7],
    ['bvwbjplbgvbhsrlpgdmjqwftvncz', 5],
    ['nppdvjthqldpwncqszvftbrmjlhg', 6],
    ['nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 10],
    ['zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 11],
])
def test_step_1(buffer, expectation):
    result = run_step_1(buffer)
    assert result == expectation


@pytest.mark.parametrize('buffer, expectation', [
    ['mjqjpqmgbljsphdztnvjfqwrcgsmlb', 19],
    ['bvwbjplbgvbhsrlpgdmjqwftvncz', 23],
    ['nppdvjthqldpwncqszvftbrmjlhg', 23],
    ['nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg', 29],
    ['zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw', 26],
])
def test_step_2(buffer, expectation):
    result = run_step_2(buffer)
    assert result == expectation
