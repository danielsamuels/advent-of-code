from year_2022.day_21 import Day

test_data = """
root: pppw + sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32
""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 152


def test_run_step_2():
    assert Day(test_data).run_step_2() == 301
