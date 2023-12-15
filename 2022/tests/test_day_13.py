import pytest

from year_2022.day_13 import run_step_1, compare, run_step_2

test_data = """
[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
""".strip()


@pytest.mark.parametrize('packet, expectation', [
    [[[1, 1, 3, 1, 1], [1, 1, 5, 1, 1]], True],
    [[[[1], [2, 3, 4]], [[1], 4]], True],
    [[[9], [[8, 7, 6]]], 1],
    [[[[4, 4], 4, 4], [[4, 4], 4, 4, 4]], True],
    [[[7, 7, 7, 7], [7, 7, 7]], 1],
    [[[], [3]], True],
    [[[[[]]], [[]]], 1],
    [[[1, [2, [3, [4, [5, 6, 7]]]], 8, 9], [1, [2, [3, [4, [5, 6, 0]]]], 8, 9]], 1],

    # Smaller tests
    [[1, 1], False],
    [[3, 5], True],
    [[[1], [1]], False],
    [[[2, 3, 4], 4], True],
    [[9, [8, 7, 6]], 1],
    [[[4, 4], [4, 4]], False],
    [[7, 7], False],
    [[[[]], []], 1],
    [[[5, 6, 7], [5, 6, 0]], 1]
])
def test_compare(packet, expectation):
    result = compare(*packet)
    if expectation is True:
        assert result < 0
    else:
        assert result >= 0


def test_run_step_1():
    assert run_step_1(test_data) == 13


def test_run_step_2():
    assert run_step_2(test_data) == 140
