import itertools
import math
import re
import sys
from typing import TypedDict, Generator

from tqdm import tqdm

from utils.dijkstra import Graph, dijkstra


class Valve(TypedDict):
    rate: int
    destinations: list[int]
    scores: range


class Day:
    def __init__(self, data: str):
        self.valves, self.names = self.process_input(data)
        self.useful_valves = set([
            index
            for index, info in self.valves.items()
            if info['rate'] > 0
        ])
        print(f'{len(self.valves)} valves, {len(self.useful_valves)} useful')
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
                     current_route: list,
                     limit: int = None) -> int:
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
            limit = limit or 1000
            if next_minute >= 30 or len(current_route) >= limit:
                route = ', '.join(self.names[v] for v in open_valves.keys())
                print(f'Route: {route} scores {score}, takes {minute} minutes')
                nested_scores.append(score)
            else:
                future_rates = self.step_1_rates(
                    score + dest_score,
                    next_minute,
                    dest,
                    {**open_valves, dest: next_minute},
                    [*current_route, (next_minute, dest, dest_score)],
                    limit,
                )
                nested_scores.append(future_rates)
        return max(nested_scores)

    def plot_all_routes(self, length_range: range = None, valves=None):
        if valves is None:
            valves = self.useful_valves

        if length_range is None:
            length_range = range(1, len(valves) + 1)

        for r in length_range:
            yield from itertools.permutations(valves, r)

    def calculate_all_route_costs(self, route_length_limit: int, starting_position: int, open_valves: set) -> Generator[tuple[list[int], int], None, None]:
        # Calculate the Dijkstra values from each valve
        ds = {
            valve: dijkstra(self.graph, valve)
            for valve in self.valves
        }
        valves = self.useful_valves - open_valves

        # What's the maximum number of valves we can visit before running out of time?
        # Note: This doesn't take into account actually opening them, just walking!
        uv_len = len(self.useful_valves)
        route_range = range(1, route_length_limit + 1)
        total_routes = math.factorial(uv_len) * route_range[-1]

        # for route in tqdm(self.plot_all_routes(route_range, valves), total=total_routes, unit_scale=True):
        for route in self.plot_all_routes(route_range, valves):
            minute = 1
            current_position = starting_position
            route_score = 0
            for target_position in route:
                if minute >= 30:
                    break

                arrival_minute = minute + ds[current_position][target_position]
                open_duration = max(30 - arrival_minute, 0)

                route_score += self.valves[target_position]['scores'][open_duration]

                current_position = target_position
                minute = arrival_minute + 1

            yield route, route_score

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

    def run_step_1_testing(self) -> int:
        max_len = math.ceil(len(self.useful_valves) / 2)
        routes = self.calculate_all_route_costs(max_len, 0, set())
        best_route = max(routes, key=lambda r: r[1])
        best_route_text = ', '.join(self.names[v] for v in best_route[0])
        print(f'Best route is {best_route_text}')
        return best_route[1]

    def run_step_2(self) -> int:
        max_len = math.ceil(len(self.useful_valves) / 2)
        start = self.names.index('AA')
        # positions = [start, start]
        open_valves = {start: 0}
        short_routes = self.step_1_rates(0, 0, start, open_valves, [(0, start, 0)], max_len)
        print(short_routes)

    def run_step_2_testing(self) -> int:
        max_len = math.ceil(len(self.useful_valves) / 2)

        # Based on the current state, what are the two best moves?
        open_valves = set()

        route_tracking = [
            [0],
            [0],
        ]
        score = 0

        # What are the best 2 options for step 1?
        routes = list(self.calculate_all_route_costs(1, 0, open_valves))
        best_routes = sorted(routes, key=lambda i: i[1], reverse=True)[:2]
        d1, d2 = best_routes[0][0][0], best_routes[1][0][0]

        s1, s2 = best_routes[0][1], best_routes[1][1]
        score += s1 + s2

        route_tracking[0].append(d1)
        open_valves.add(d1)
        route_tracking[1].append(d2)
        open_valves.add(d2)

        while len(open_valves) < len(self.useful_valves):
            # What are the best 2 options for step 2?
            routes_0 = list(self.calculate_all_route_costs(1, route_tracking[0][-1], open_valves))
            best_route_0 = sorted(routes_0, key=lambda i: i[1], reverse=True)[0]
            best_route_0_pos = best_route_0[0][0]
            route_tracking[0].append(best_route_0_pos)
            score += best_route_0[1]

            open_valves.add(best_route_0_pos)

            routes_1 = list(self.calculate_all_route_costs(1, route_tracking[1][-1], open_valves))
            best_route_1 = sorted(routes_1, key=lambda i: i[1], reverse=True)[0]
            best_route_1_pos = best_route_1[0][0]
            route_tracking[1].append(best_route_1_pos)
            score += best_route_1[1]

            open_valves.add(best_route_1)

        print(open_valves, route_tracking)
        print('Route 1:', ', '.join(self.names[v] for v in route_tracking[0]))
        print('Route 2:', ', '.join(self.names[v] for v in route_tracking[1]))
        return score


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        data = f.read()

    day = Day(data)

    # 2359
    # result = day.run_step_1()
    # print(f'Step 1: {result}')

    # 3882 is too high
    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
