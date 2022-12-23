import pytest

from year_2022.day_22 import Day

test_data = """
        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5""".strip('\n')


def test_run_step_1():
    assert Day(test_data).run_step_1() == 6032


@pytest.mark.parametrize('instructions, position, direction', [
    ['1R', (9, 0), 'D'],
    ['2R', (10, 0), 'D'],
    ['3R', (10, 0), 'D'],
    ['1L', (9, 0), 'U'],
    ['2L', (10, 0), 'U'],
    ['1L1L1L1L', (8, 0), 'R']
])
def test_run_step_1_alternate(instructions, position, direction):
    ds = {'R': 0, 'D': 1, 'L': 2, 'U': 3}
    # The final password is the sum of 1000 times the row, 4 times the column, and the facing.
    # row=1, column=10, facing=1
    # (1000*1) + (4*10) + 1
    # 1000 + 40 = 1041

    column, row = position
    expectation = sum([
        1000 * (row + 1),
        4 * (column + 1),
        ds[direction],
    ])

    data = test_data[:-17] + '\n\n' + instructions
    assert 0 == expectation


def test_run_step_2():
    assert Day(test_data).run_step_2() == 0
