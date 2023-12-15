from year_2022.day_23 import Day

test_data = """
....#..
..###.#
#...#.#
.#...##
#.###..
##.#.##
.#..#..
""".strip('\n')

simple_example = """
.....
..##.
..#..
.....
..##.
.....
""".strip('\n')


def test_simple_example():
    day = Day(simple_example)
    day.simulate_rounds(3)
    """
    Final position should be this:
    
    ..#..
    ....#
    #....
    ....#
    .....
    ..#..
    """
    assert day.step_1_score == 25


def test_run_step_1():
    assert Day(test_data).run_step_1() == 110


def test_run_step_2():
    assert Day(test_data).run_step_2() == 20
