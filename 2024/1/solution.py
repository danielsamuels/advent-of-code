from aocd import data, submit

class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.left_list: list[int] = []
        self.right_list: list[int] = []

        for line in self.data:
            left, right = line.split()
            self.left_list.append(int(left))
            self.right_list.append(int(right))

    def run_step_1(self):
        left_list = sorted(self.left_list)
        right_list = sorted(self.right_list)

        return sum([
            abs(left - right)
            for left, right in zip(left_list, right_list)
        ])

    def run_step_2(self):
        answer = 0
        for val in self.left_list:
            answer += val * self.right_list.count(val)

        return answer
