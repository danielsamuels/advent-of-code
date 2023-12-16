from solution import Day, Grid
from utils.grid import Direction

test_data = """
.|...\\....
|.-.\\.....
.....|-...
........|.
..........
.........\\
..../.\\\\..
.-.-/..|..
.|....-|.\\
..//.|....
""".strip()


def test_run_step_1():
    day = Day(test_data)
    result = day.run_step_1()
    assert result == 46


def test_grid_visited_cells():
    grid = Grid(test_data.splitlines(), (-1, 0), Direction.EAST)
    grid.exhaust_queue()
    assert grid.visited_cells == {
        (0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0),
        (1, 1), (5, 1),
        (1, 2), (5, 2), (6, 2), (7, 2), (8, 2), (9, 2),
        (1, 3), (5, 3), (6, 3),
        (1, 4), (5, 4), (6, 4),
        (1, 5), (5, 5), (6, 5),
        (1, 6), (4, 6), (5, 6), (6, 6), (7, 6),
        (0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
        (1, 8), (2, 8), (3, 8), (4, 8), (5, 8), (6, 8), (7, 8),
        (1, 9), (5, 9), (7, 9),
    }


def test_run_step_2():
    assert Day(test_data).run_step_2() == 51
