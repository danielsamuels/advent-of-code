import functools
import string

DIGITS = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
}
DIGIT_WORDS = list(DIGITS.keys())
DIGIT_NUMBERS = list(string.digits)[1:]
DIGIT_OPTIONS = DIGIT_WORDS + DIGIT_NUMBERS


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def run_step_1(self) -> int:
        results = []
        for line in self.data:
            first_number = last_number = None
            for char in line:
                if char.isdigit():
                    if first_number is None:
                        first_number = char

                    last_number = char

            results.append(int(first_number + last_number))

        return sum(results)

    def run_step_2(self) -> int:
        results = []
        for line in self.data:
            lower = {s: line.find(s) for s in DIGIT_OPTIONS if line.find(s) != -1}
            upper = {s: line.rfind(s) for s in DIGIT_OPTIONS if line.find(s) != -1}

            first_number = functools.reduce(lambda a, b: a if a[1] < b[1] else b, lower.items())[0]
            last_number = functools.reduce(lambda a, b: a if a[1] > b[1] else b, upper.items())[0]

            if first_number in DIGIT_WORDS:
                first_number = DIGITS[first_number]

            if last_number in DIGIT_WORDS:
                last_number = DIGITS[last_number]

            results.append(int(first_number + last_number))

        return sum(results)
