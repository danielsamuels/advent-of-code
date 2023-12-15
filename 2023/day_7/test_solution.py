import pytest

from solution import Day, HandType, Hand, Card

test_data = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
""".strip()


@pytest.mark.parametrize('hand,expected_type', [
    ('AAAAA', HandType.FIVE_OF_A_KIND),
    ('AA8AA', HandType.FOUR_OF_A_KIND),
    ('23332', HandType.FULL_HOUSE),
    ('TTT98', HandType.THREE_OF_A_KIND),
    ('T55J5', HandType.THREE_OF_A_KIND),
    ('QQQJA', HandType.THREE_OF_A_KIND),
    ('23432', HandType.TWO_PAIR),
    ('KK677', HandType.TWO_PAIR),
    ('KTJJT', HandType.TWO_PAIR),
    ('A23A4', HandType.ONE_PAIR),
    ('32T3K', HandType.ONE_PAIR),
    ('23456', HandType.HIGH_CARD),
])
def test_hand_type(hand, expected_type):
    assert Hand(hand).hand_type == expected_type

@pytest.mark.parametrize('hand,expected_type', [
    ('JJJJJ', HandType.FIVE_OF_A_KIND),
    ('AAAAA', HandType.FIVE_OF_A_KIND),
    ('JAAAA', HandType.FIVE_OF_A_KIND),
    ('AJAAA', HandType.FIVE_OF_A_KIND),
    ('AAJAA', HandType.FIVE_OF_A_KIND),
    ('AAAJA', HandType.FIVE_OF_A_KIND),
    ('AAAAJ', HandType.FIVE_OF_A_KIND),

    ('AA8AA', HandType.FOUR_OF_A_KIND),
    ('TTTT8', HandType.FOUR_OF_A_KIND),
    ('JTTT8', HandType.FOUR_OF_A_KIND),
    ('TJTT8', HandType.FOUR_OF_A_KIND),
    ('TTJT8', HandType.FOUR_OF_A_KIND),
    ('TTTJ8', HandType.FOUR_OF_A_KIND),
    ('TTT8J', HandType.FOUR_OF_A_KIND),
    ('T55J5', HandType.FOUR_OF_A_KIND),
    ('KTJJT', HandType.FOUR_OF_A_KIND),
    ('QQQJA', HandType.FOUR_OF_A_KIND),
    ('QJJQ2', HandType.FOUR_OF_A_KIND),
    ('JJQJ4', HandType.FOUR_OF_A_KIND),
    ('JJ2J9', HandType.FOUR_OF_A_KIND),
    ('JTJ55', HandType.FOUR_OF_A_KIND),

    ('23332', HandType.FULL_HOUSE),
    ('J2233', HandType.FULL_HOUSE),
    ('2J233', HandType.FULL_HOUSE),
    ('22J33', HandType.FULL_HOUSE),
    ('223J3', HandType.FULL_HOUSE),
    ('2233J', HandType.FULL_HOUSE),
    ('22333', HandType.FULL_HOUSE),
    ('25J52', HandType.FULL_HOUSE),

    ('AJKJ4', HandType.THREE_OF_A_KIND),
    ('TTT98', HandType.THREE_OF_A_KIND),
    ('JTT98', HandType.THREE_OF_A_KIND),
    ('TJT98', HandType.THREE_OF_A_KIND),
    ('TTJ98', HandType.THREE_OF_A_KIND),
    ('TT9J8', HandType.THREE_OF_A_KIND),
    ('TT98J', HandType.THREE_OF_A_KIND),
    ('T9T8J', HandType.THREE_OF_A_KIND),
    ('T98TJ', HandType.THREE_OF_A_KIND),
    ('T98JT', HandType.THREE_OF_A_KIND),
    ('TQJQ8', HandType.THREE_OF_A_KIND),

    ('23432', HandType.TWO_PAIR),
    ('KK677', HandType.TWO_PAIR),
    ('KK677', HandType.TWO_PAIR),

    ('32T3K', HandType.ONE_PAIR),
    ('A23A4', HandType.ONE_PAIR),
    ('32T3K', HandType.ONE_PAIR),
    ('J2345', HandType.ONE_PAIR),
    ('2J345', HandType.ONE_PAIR),
    ('23J45', HandType.ONE_PAIR),
    ('234J5', HandType.ONE_PAIR),
    ('2345J', HandType.ONE_PAIR),
    ('5TK4J', HandType.ONE_PAIR),

    ('23456', HandType.HIGH_CARD),
])
def test_hand_type_jokers(hand, expected_type):
    assert Hand(hand, jokers=True).hand_type == expected_type


@pytest.mark.parametrize('first,second', [
    ('33332', '2AAAA'),
    ('77888', '77788'),
])
def test_hand_sorting(first, second):
    assert Hand(first) > Hand(second)

@pytest.mark.parametrize('first,second', [
    ('QQQQ2', 'JKKK2'),
    ('QQQJA', 'T55J5'),
    ('KTJJT', 'QQQJA'),
    ('KTJJT', 'T55J5'),
    ('AAAAA', 'JJJJJ'),
    ('AAAAA', 'JAAAA'),
    ('KKKKK', 'JAAAA'),
    ('JAAAA', 'JKKKK'),
    ('JAAA2', 'JKKK2'),
    ('JAA22', 'JKK22'),
    ('AA22J', 'JKK22'),
    ('2233J', '223J3'),
    ('2233J', '223J4'),
    ('2234J', '223J4'),

    # 5>4
    ('JJJJJ', 'AAAJ2'),
    # 4>Full
    ('AAAJ2', 'AA22J'),
    # Full>3
    ('AA22J', 'A232J'),
    # 3>2
    ('A232J', 'AJ233'),
    # 2>1
    ('AJ233', 'A234J'),
    # 1>H
    ('A234J', 'A2345'),

    ('QJJQ3', 'QJJQ2'),

])
def test_hand_sorting_jokers(first, second):
    assert Hand(first, jokers=True) > Hand(second, jokers=True)
    assert Hand(second, jokers=True) < Hand(first, jokers=True)


@pytest.mark.parametrize('first,second,jokers', [
    ('A', 'K', True),
    ('A', 'K', False),
    ('A', 'J', True),
    ('A', 'J', False),
    ('T', 'J', True),
    ('J', 'T', False),
])
def test_card_sorting(first, second, jokers):
    assert Card(first, jokers=jokers) > Card(second, jokers=jokers)

def test_run_step_1():
    assert Day(test_data).run_step_1() == 6440


def test_run_step_2():
    assert Day(test_data).run_step_2() == 5905

additional_data = """
2345A 2
2345J 5
J345A 3
32T3K 7
T55J5 17
KK677 11
KTJJT 23
QQQJA 19
JJJJJ 29
JAAAA 37
AAAAJ 43
AAAAA 53
2AAAA 13
2JJJJ 41
JJJJ2 31
""".strip()

def test_run_step_2_additional():
    assert Day(additional_data).run_step_2() == 3667
