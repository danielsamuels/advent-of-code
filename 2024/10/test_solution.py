from solution import Day

small_test_data = """
0123
1234
8765
9876
""".strip()

large_test_data = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""".strip()


def test_run_step_1_small():
    assert Day(small_test_data).run_step_1() == 1


def test_run_step_1_large():
    assert Day(large_test_data).run_step_1() == 36


def test_run_step_2():
    assert Day(large_test_data).run_step_2() == 81
