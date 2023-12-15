from collections import defaultdict

from utils.data import get_data


def hash_word(word):
    word_score = 0
    for char in word:
        word_score += ord(char)
        word_score *= 17
        word_score %= 256
    return word_score


class Day:
    def __init__(self, data: str):
        self.data = data.split(',')

    def run_step_1(self) -> int:
        # 513643
        return sum(hash_word(word) for word in self.data)

    def run_step_2(self) -> int:
        boxes = defaultdict(dict)

        for word in self.data:
            sign = '-' if '-' in word else '='
            label, focal_length = word.split(sign)
            box = hash_word(label)

            if sign == '-':
                if label in boxes[box]:
                    del boxes[box][label]

            else:
                boxes[box][label] = focal_length

        # 265345
        return sum([
            (box_num + 1) * (lens_index + 1) * int(focal_length)
            for box_num, lenses in boxes.items()
            for lens_index, focal_length in enumerate(lenses.values())
        ])


if __name__ == "__main__":
    data = get_data(__file__)

    day = Day(data)
    print(f'Step 1: {day.run_step_1()}')
    print(f'Step 2: {day.run_step_2()}')
