"""
For example, suppose the Elves finish writing their items' Calories and end up with the following list:

```
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
```

This list represents the Calories of the food carried by five Elves:

The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
The second Elf is carrying one food item with 4000 Calories.
The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
The fifth Elf is carrying one food item with 10000 Calories.
In case the Elves get hungry and need extra snacks, they need to know which Elf to ask:
    they'd like to know how many Calories are being carried by the Elf carrying the most Calories.
In the example above, this is 24000 (carried by the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?
"""


def run(data: str):
    elves: list[str] = data.strip().split('\n\n')
    elf_loads = [sum(map(int, elf.split('\n'))) for elf in elves]
    sorted_loads = sorted(elf_loads, reverse=True)

    print('Highest: ', sorted_loads[0])
    print('Sum of top 3: ', sum(sorted_loads[0:3]))


if __name__ == '__main__':
    with open('data/day_1.txt', 'r') as f:
        data = f.read()

    run(data)
