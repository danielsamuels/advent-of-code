from year_2022.day_5 import run_step_1, run_step_2

test_data = """
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
""".strip('\n')


def test_day_5_step_1():
    output = run_step_1(test_data)
    assert output == 'CMZ'


def test_day_5_step_2():
    output = run_step_2(test_data)
    assert output == 'MCD'