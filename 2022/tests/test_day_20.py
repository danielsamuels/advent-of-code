from year_2022.day_20 import Day

test_data = """
1
2
-3
3
-2
0
4
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 3


def test_others():
    numbers = [5, 1, -1, 0, 2]
    # [5, 1, -1, 0, 2]
    # [1, 5, -1, 0, 2]
    # [5, 1, -1, 0, 2]
    # [5, -1, 1, 0, 2]
    # [5, -1, 1, 0, 2]
    # [5, -1, 2, 1, 0]
    result = Day('\n'.join(str(n) for n in numbers)).process_inputs()
    result = [v[1] for v in result]
    assert result == [
        5, -1, 2, 1, 0
    ]


def test_run_step_2():
    assert Day(test_data, step=2).run_step_2() == 1623178306
