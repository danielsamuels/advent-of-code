# advent-of-code-2022

https://adventofcode.com/2022

File base:
```python
class Day:
    def __init__(self):
        test_filename = __file__.split('\\')[-1].split('.py')[0]
        with open(f'data/{test_filename}.txt', 'r') as f:
            data = f.read()

        print(data)    

    def run_step_1(self) -> int: ...
    def run_step_2(self) -> int: ...


if __name__ == "__main__":
    day = Day()

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')

```

Test base:

```python
from year_2022.day_16 import Day

test_data = """""".strip()


def test_run_step_1():
    assert Day(test_data).run_step_1() == 0


def test_run_step_2():
    assert Day(test_data).run_step_2() == 0

```