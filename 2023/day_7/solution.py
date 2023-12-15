import enum
import operator
from collections import Counter

CARD_TYPES = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
CARD_TYPES_JOKER = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']

class HandType(enum.IntEnum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1

class Card:
    def __init__(self, value: str, *, jokers: bool = False):
        self.value = value
        self.jokers = jokers

    def __eq__(self, other):
        # A joker will always be equal to another single card
        # However, this means it's possible for a==b==c _and_ a!=c
        if self.jokers and 'J' in [self.value, other.value]:
            return True
        return self.value == other.value

    def __gt__(self, other):
        if self.jokers:
            return CARD_TYPES_JOKER.index(self.value) < CARD_TYPES_JOKER.index(other.value)
        return CARD_TYPES.index(self.value) < CARD_TYPES.index(other.value)

    def __lt__(self, other):
        if self.jokers:
            return CARD_TYPES_JOKER.index(self.value) > CARD_TYPES_JOKER.index(other.value)
        return CARD_TYPES.index(self.value) > CARD_TYPES.index(other.value)

    def __hash__(self):
        return CARD_TYPES.index(self.value)

    def __repr__(self):
        return self.value


class Hand:
    def __init__(self, cards: str, *, jokers: bool = False):
        self.value = cards
        self.cards: list[Card] = [Card(value, jokers=jokers) for value in cards]
        self.jokers = jokers

    def x_of_a_kind(self, n):
        if self.value == 'JJJJJ':
            return n == 5

        common = Counter(self.value.replace('J', '')).most_common()

        if self.jokers:
            v = self.value.replace('J', common[0][0])
            common = Counter(v).most_common()

        return common[0][1] == n

    @property
    def hand_type(self):
        c = self.cards
        s = list(sorted(c))
        u = set(c)

        if self.x_of_a_kind(5):
            return HandType.FIVE_OF_A_KIND

        if self.x_of_a_kind(4):
            return HandType.FOUR_OF_A_KIND

        if any([
            s[0] == s[1] and s[2] == s[3] == s[4],
            s[0] == s[1] == s[2] and s[3] == s[4],
        ]):
            return HandType.FULL_HOUSE

        if self.x_of_a_kind(3):
            return HandType.THREE_OF_A_KIND

        if any([
            s[0] == s[1] and s[2] == s[3],
            s[0] == s[1] and s[3] == s[4],
            s[1] == s[2] and s[3] == s[4],
        ]):
            if self.jokers:
                assert 'J' not in self.value
            return HandType.TWO_PAIR

        if any([
            s[0] == s[1],
            s[1] == s[2],
            s[2] == s[3],
            s[3] == s[4],
        ]):
            return HandType.ONE_PAIR

        if self.jokers:
            assert 'J' not in self.value
        return HandType.HIGH_CARD

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        if self.hand_type == other.hand_type:
            for first, second in zip(self.cards, other.cards):
                if first.value == second.value:
                    continue

                return first > second

        return self.hand_type > other.hand_type

    def __lt__(self, other):
        if self.hand_type == other.hand_type:
            for first, second in zip(self.cards, other.cards):
                if first.value == second.value:
                    continue

                return first < second

        return self.hand_type < other.hand_type

    def __repr__(self):
        return f'{self.cards} ({self.hand_type.name})'

class Day:
    def __init__(self, data: str):
        self.data = [l.split() for l in data.splitlines()]

    def run_step_1(self) -> int:
        hands = {
            cards: {
                'hand': Hand(cards),
                'bid': bid,
            }
            for cards, bid in self.data
        }

        sorted_hands = sorted(hands.values(), key=operator.itemgetter('hand'))

        result = 0
        for rank, hand in enumerate(sorted_hands):
            score = (rank + 1) * int(hand['bid'])
            result += score

        return result


    def run_step_2(self) -> int:
        hands = {
            cards: {
                'hand': Hand(cards, jokers=True),
                'bid': bid,
            }
            for cards, bid in self.data
        }

        sorted_hands = sorted(hands.values(), key=operator.itemgetter('hand'))

        result = 0
        for rank, hand in enumerate(sorted_hands):
            score = (rank + 1) * int(hand['bid'])
            result += score

        return result


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
