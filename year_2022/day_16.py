import re
from typing import TypedDict

from utils.dijkstra import Graph, dijkstra


class Valve(TypedDict):
    rate: int
    destinations: list[int]
    scores: range


class Day:
    def __init__(self, data: str):
        self.valves, self.names = self.process_input(data)
        self.graph = self.build_graph()
        self.routes = {}

    @staticmethod
    def process_input(data: str) -> tuple[dict[int, Valve], list[str]]:
        valves = re.findall(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ((?:\w+(?:, )?)+)', data)
        valve_indexes = {
            valve: index
            for index, [valve, _, _] in enumerate(valves)
        }
        valve_names = [valve[0] for valve in valves]
        return {
            valve_indexes[valve]: {
                'rate': int(rate),
                'destinations': [
                    valve_indexes[dest]
                    for dest in destinations.split(', ')
                ],
                'scores': [int(rate) * m for m in range(30)],
            }
            for valve, rate, destinations in valves
        }, valve_names

    def build_graph(self):
        graph = Graph(len(self.valves))
        for source, info in self.valves.items():
            for destination in info['destinations']:
                graph.add_one_way_edge(source, destination, 1)

        return graph

    def step_1_rates(self,
                     score: int,
                     minute: int,
                     current_position: int,
                     open_valves: dict[int, int],
                     current_route: list) -> int:
        # Based on how long it would take to get to a valve and open it
        # What is it the highest possible flow rate available?
        d = dijkstra(self.graph, current_position)
        # Which valves are not yet open and are useful to visit?
        available_valves = set([
            index
            for index, info in self.valves.items()
            if info['rate'] > 0
        ]) - set(open_valves.keys())

        rates = {}
        for valve in available_valves:
            index = 30 - (minute + d[valve]) - 1
            scores = self.valves[valve]['scores']
            rates[valve] = scores[index]

        # There's nowhere else to go
        if not rates:
            route = ', '.join(self.names[v] for v in open_valves.keys())
            print(f'Route: {route} scores {score}, takes {minute} minutes')
            return score

        nested_scores = []
        for dest, dest_score in rates.items():
            next_minute = minute + d[dest] + 1
            if next_minute >= 30:
                nested_scores.append(score)
            else:
                future_rates = self.step_1_rates(
                    score + dest_score,
                    next_minute,
                    dest,
                    {**open_valves, dest: next_minute},
                    [*current_route, (next_minute, dest, dest_score)]
                )
                nested_scores.append(future_rates)
        return max(nested_scores)

    def run_step_1(self) -> int:
        current_position = self.names.index('AA')
        open_valves = {current_position: 0}
        return self.step_1_rates(
            0,
            0,
            current_position,
            open_valves,
            [(0, current_position, 0)],
        )

    def run_step_2(self) -> int:
        return 0


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        data = f.read()

    day = Day(data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
