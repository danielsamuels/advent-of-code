from year_2022.day_18 import Day

test_data = """
2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5
""".strip()


def test_simple_example():
    simple_data = """1,1,1\n2,1,1"""
    assert Day(simple_data).run_step_1() == 10


def test_run_step_1():
    assert Day(test_data).run_step_1() == 64


def test_run_step_2():
    assert Day(test_data).run_step_2() == 58


def test_interior_cubes():
    assert Day(test_data).interior_cubes() == [
        (2, 2, 5),
    ]
