import pytest

from solution import Day

test_data = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'


@pytest.mark.parametrize('string, expected_score', [
    ('HASH', 52),
    (test_data, 1320),
])
def test_run_step_1(string, expected_score):
    assert Day(string).run_step_1() == expected_score


def test_run_step_2():
    assert Day(test_data).run_step_2() == 145
