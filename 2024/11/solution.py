from collections import defaultdict


class Day:
    def __init__(self, data: str):
        self.data = defaultdict(int)

        for value in data.split():
            self.data[value] += 1

    def blink(self, stones: dict) -> dict:
        old_stones = dict(stones)
        new_stones = defaultdict(int)

        for stone, count in old_stones.items():
            if stone == "0":
                new_stones["1"] += count
            elif len(stone) % 2 == 0:
                new_1 = str(int(stone[:len(stone) // 2]))
                new_2 = str(int(stone[len(stone) // 2:]))
                new_stones[new_1] += count
                new_stones[new_2] += count
            else:
                value = str(int(stone) * 2024)
                new_stones[value] += count

        return new_stones

    def calculate(self, iterations):
        stones = dict(self.data)

        for _ in range(iterations):
            stones = self.blink(stones)

        return sum(stones.values())

    def run_step_1(self) -> int:
        return self.calculate(25)

    def run_step_2(self) -> int:
        return self.calculate(75)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
