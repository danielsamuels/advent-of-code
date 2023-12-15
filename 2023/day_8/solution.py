import itertools
import math
from typing import Callable


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()
        self.instruction = self.data.pop(0)
        # Remove the empty line
        self.data.pop(0)

        self.nodes = {}
        for node in self.data:
            key, values = node.split(' = ')
            self.nodes[key] = {'L': values[1:4], 'R': values[6:9]}

    def run_cycle(self, start_node: str, check_fn: Callable):
        current_node = start_node
        for step, instruction in enumerate(itertools.cycle(self.instruction)):
            current_node = self.nodes[current_node][instruction]
            if check_fn(current_node):
                return step + 1


    def run_step_1(self) -> int:
        return self.run_cycle('AAA', lambda n: n == 'ZZZ')


    def run_step_2(self) -> int:
        current_nodes = [
            node
            for node in self.nodes.keys()
            if node.endswith('A')
        ]
        # Run each node individually to get a cycle length
        # Then assume there's a LCM where they coalesce
        cycle_lengths = {
            node: self.run_cycle(node, lambda n: n.endswith('Z'))
            for node in current_nodes
        }
        return math.lcm(*cycle_lengths.values())


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
