import pytest

from year_2022.day_8 import transform_input, item_visible, Visible, run_step_1, calculate_scenic_score

test_data = """
30373
25512
65332
33549
35390
""".strip()


def test_transform_input():
    assert transform_input(test_data) == [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0],
    ]


@pytest.mark.parametrize('x, y, expectation', [
    [0, 0, {Visible.LEFT, Visible.TOP}],
    [0, 4, {Visible.LEFT, Visible.BOTTOM}],
    [4, 0, {Visible.TOP, Visible.RIGHT}],
    [4, 4, {Visible.BOTTOM, Visible.RIGHT}],
    [1, 1, {Visible.LEFT, Visible.TOP}],
    [2, 1, {Visible.TOP, Visible.RIGHT}],
    [3, 1, set()],
    [1, 2, {Visible.RIGHT}],
    [2, 2, set()],
    [3, 2, {Visible.RIGHT}],
    [1, 3, set()],
    [2, 3, {Visible.LEFT, Visible.BOTTOM}],
    [3, 3, set()],
])
def test_item_visible(x, y, expectation):
    data = transform_input(test_data)
    assert item_visible(data, x, y) == expectation


@pytest.mark.parametrize('x, y, expectation', [
    [2, 1, 4],
    [2, 3, 8],
])
def test_calculate_scenic_score(x, y, expectation):
    data = transform_input(test_data)
    assert calculate_scenic_score(data, x, y) == expectation


def test_run_step_1():
    assert run_step_1(test_data) == 21
