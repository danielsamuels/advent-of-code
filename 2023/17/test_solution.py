from solution import Day

test_data = """
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 102


def test_run_step_2():
    assert Day(test_data).run_step_2() == 94


def test_run_step_2_example_2():
    data = """
111111111111
999999999991
999999999991
999999999991
999999999991
""".strip()
    assert Day(data).run_step_2() == 71
