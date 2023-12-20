from solution import Day

test_data_1 = """
broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a
""".strip()

test_data_2 = """
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
""".strip()


def test_run_step_1_ex1():
    assert Day(test_data_1).run_step_1() == 32000000


def test_run_step_1_ex2():
    day = Day(test_data_2)
    without_cache_result = day.run_step_1()
    assert day.low_sent == 4250
    assert day.high_sent == 2750
    assert without_cache_result == 11687500
