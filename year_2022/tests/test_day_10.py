import pytest

from year_2022.day_10 import run_steps, run_cycles, build_crt

test_data = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
""".strip()

def test_run_cycles_example():
    data = """
    noop
    addx 3
    addx -5
    """.strip()
    cycles, _ = run_cycles(data)
    assert len(cycles) == 5
    assert cycles == {
        1: {'x': 1, 'strength': 1},
        2: {'x': 1, 'strength': 2},
        3: {'x': 1, 'strength': 3},
        4: {'x': 4, 'strength': 16},
        5: {'x': 4, 'strength': 20},
    }


@pytest.mark.parametrize('cycle, x, strength', [
    [20, 21, 420],
    [60, 19, 1140],
    [100, 18, 1800],
    [140, 21, 2940],
    [180, 16, 2880],
    [220, 18, 3960],
])
def test_run_cycles_test_data(cycle, x, strength):
    cycles, _ = run_cycles(test_data)
    assert cycles[cycle]['x'] == x
    assert cycles[cycle]['strength'] == strength


def test_build_crt():
    _, crt = run_cycles(test_data)
    assert build_crt(crt) == """
##..##..##..##..##..##..##..##..##..##..
###...###...###...###...###...###...###.
####....####....####....####....####....
#####.....#####.....#####.....#####.....
######......######......######......####
#######.......#######.......#######.....
""".strip()


def test_run_steps():
    value = run_steps(test_data)
    assert value == 13140
