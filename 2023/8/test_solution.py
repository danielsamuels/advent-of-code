from solution import Day

test_data = """
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
""".strip()

test_data_2 = """
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 2

def test_run_step_1_second():
    assert Day(test_data_2).run_step_1() == 6


step_2_test_data = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
""".strip()

def test_run_step_2():
    assert Day(step_2_test_data).run_step_2() == 6
