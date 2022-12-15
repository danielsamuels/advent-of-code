from year_2022.day_14 import run_step_1, process_input, run_step_2

test_data = """
498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9
""".strip()


def test_process_input():
    assert process_input(test_data) == {
        # Wall 1
        (498, 4),
        (498, 5),
        (498, 6),
        (497, 6),
        (496, 6),
        # Wall 2
        (503, 4),
        (502, 4),
        (502, 5),
        (502, 6),
        (502, 7),
        (502, 8),
        (502, 9),
        (501, 9),
        (500, 9),
        (499, 9),
        (498, 9),
        (497, 9),
        (496, 9),
        (495, 9),
        (494, 9),
    }


def test_run_step_1():
    assert run_step_1(test_data) == 24


def test_run_step_2():
    assert run_step_2(test_data) == 93
