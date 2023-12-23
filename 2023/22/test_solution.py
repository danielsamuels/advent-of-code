import string

from solution import Day, Brick

test_data = """
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
""".strip()


def test_run_step_1():
    day = Day(test_data)

    b = {
        chr(int(brick.label) + 65): brick
        for brick in day.bricks
    }

    for brick in day.bricks:
        assert brick.can_move_down is False

    assert b['A'].start == (1, 0, 1)
    assert b['A'].end == (1, 2, 1)

    assert b['B'].start == (0, 0, 2)
    assert b['B'].end == (2, 0, 2)

    assert b['D'].start == (0, 0, 3)
    assert b['D'].end == (0, 2, 3)

    assert b['A'].supported_by == []
    assert b['A'].supporting == [b['B'], b['C']]
    assert b['A'].can_be_disintegrated is False

    assert b['B'].supported_by == [b['A']]
    assert b['B'].supporting == [b['D'], b['E']]
    assert b['B'].can_be_disintegrated is True

    assert b['C'].supported_by == [b['A']]
    assert b['C'].supporting == [b['D'], b['E']]
    assert b['B'].can_be_disintegrated is True

    assert b['D'].supported_by == [b['B'], b['C']]
    assert b['D'].supporting == [b['F']]
    assert b['D'].can_be_disintegrated is True

    assert b['E'].supported_by == [b['B'], b['C']]
    assert b['E'].supporting == [b['F']]
    assert b['E'].can_be_disintegrated is True

    assert b['F'].supported_by == [b['D'], b['E']]
    assert b['F'].supporting == [b['G']]
    assert b['F'].can_be_disintegrated is False

    assert b['G'].supported_by == [b['F']]
    assert b['G'].supporting == []
    assert b['G'].can_be_disintegrated is True

    assert day.run_step_1() == 5


def test_run_step_2():
    day = Day(test_data)
    day.settle_bricks()

    b: dict[str, Brick] = {
        chr(int(brick.label) + 65): brick
        for brick in day.bricks
    }

    assert b['A'].disintegration_result == 6
    assert b['B'].disintegration_result == 0
    assert b['C'].disintegration_result == 0
    assert b['D'].disintegration_result == 0
    assert b['E'].disintegration_result == 0
    assert b['F'].disintegration_result == 1
    assert b['G'].disintegration_result == 0

    assert day.run_step_2() == 7
