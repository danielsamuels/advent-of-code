import re


class Day:
    def __init__(self, data: str):
        self.data = data

    def calculate(self, item) -> int:
        return int(item[0]) * int(item[1])

    def run_step_1(self) -> int:
        muls = re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', self.data)
        return sum(self.calculate(item) for item in muls)

    def run_step_2(self) -> int:
        """
        >>> s = "abcdon't()somethingdo()morestuffdon't()somedo()abc123"
        >>> [sub.split("do()")[-1] for sub in s.split("don't()")]
        ['abc', 'morestuff', 'abc123']
        """
        first, *others = self.data.split("don't()")

        to_process = [first]
        for part in others:
            # don't() -> "blahblahblahsomethingdo()thensomeusefulstuff"
            _, *useful = part.split("do()", 1)

            if useful:
                to_process.append(useful[0])

        return sum([
            self.calculate(item)
            for part in to_process
            for item in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', part)
        ])


if __name__ == '__main__':
    from aocd import data
    # print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
