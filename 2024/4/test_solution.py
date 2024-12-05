from solution import Day

test_data = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 18


def test_run_step_2():
    assert Day(test_data).run_step_2() == 9
