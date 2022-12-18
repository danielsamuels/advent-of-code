from year_2022.day_17 import Day, ROCK_TYPES

test_data = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"


def test_run_step_1():
    assert Day(test_data).run_process(2022) == 3068


def test_run_step_2():
    assert Day(test_data).run_process(1_000_000_000_000) == 1514285714288


def test_new_rock():
    day = Day('')
    expectation = [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0]
    for i in expectation:
        rock = next(day.rock)
        assert rock.points == ROCK_TYPES[i]
