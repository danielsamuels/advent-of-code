import heapq
import math
from collections import deque

from utils.dijkstra import Graph, dijkstra, neighbours
from utils.grid import parse_grid, Direction, DROP, cardinal_point_occupation, dict_grid_to_list, compute_new_position


class Day:
    grid = {}
    grid_width: int
    grid_height: int

    graph: Graph

    def __init__(self, data: str):
        self.data = data.splitlines()

    def setup(self, ignore_slopes: bool = False):
        mapping = {
            '#': DROP,
            '.': '.',
            '^': Direction.NORTH,
            'v': Direction.SOUTH,
            '<': Direction.WEST,
            '>': Direction.EAST,
        }
        if ignore_slopes:
            mapping['^'] = '.'
            mapping['v'] = '.'
            mapping['<'] = '.'
            mapping['>'] = '.'

        self.grid = parse_grid(self.data, mapping, add_index=True)
        self.grid_width, self.grid_height = len(self.data[0]), len(self.data)
        self.graph = self.build_graph()

    def reduce_graph(self, graph: Graph) -> Graph:
        # Find any nodes which only have two neighbours
        print('Reducing size of graph')

        def build_relations():
            for u, others in enumerate(graph.edges):
                neighbs = [
                    v
                    for v, w in enumerate(others)
                    if w != -1
                ]
                if len(neighbs) == 2:
                    yield u, neighbs

        neighbourly_relations = build_relations()

        reductions = 0
        for node, n in neighbourly_relations:
            # Create a new edge from each of the two neighbours
            # Forwards..
            # print([
            #     graph.edges[n[0]][node],
            #     graph.edges[node][n[0]],
            #     graph.edges[n[1]][node],
            #     graph.edges[node][n[1]],
            # ])

            assert graph.edges[n[0]][node] != -1
            assert graph.edges[node][n[1]] != -1
            assert graph.edges[n[1]][node] != -1
            assert graph.edges[node][n[0]] != -1
            fwd_weight = graph.edges[n[0]][node] + graph.edges[node][n[1]]
            rev_weight = graph.edges[n[1]][node] + graph.edges[node][n[0]]
            graph.add_one_way_edge(n[0], n[1], weight=fwd_weight)
            graph.add_one_way_edge(n[1], n[0], weight=rev_weight)

            graph.remove_edge(n[0], node)
            graph.remove_edge(node, n[1])

            # Backwards..
            graph.remove_edge(n[1], node)
            graph.remove_edge(node, n[0])

            assert n[1] in neighbours(graph, n[0], [])
            assert n[0] in neighbours(graph, n[1], [])

            reductions += 1

        if reductions:
            return self.reduce_graph(graph)
        return graph

    def build_graph(self):
        print('Initializing graph')
        graph = Graph(self.grid_width * self.grid_height)
        list_grid = dict_grid_to_list(self.grid, self.grid_width, self.grid_height)

        print('Building graph')
        for position, data in self.grid.items():
            value = data['value']
            # If we're forced to move, add those in
            if isinstance(value, Direction):
                dest = compute_new_position(position, value)
                graph.add_one_way_edge(data['index'], self.grid[dest]['index'])
                continue

            card = cardinal_point_occupation(list_grid, position)
            for card_info in card.values():
                dest = card_info['position']
                graph.add_one_way_edge(data['index'], self.grid[dest]['index'])

        return self.reduce_graph(graph)

    def find_longest_route(self) -> int:
        print('Finding longest route')
        start_index = self.grid[(1, 0)]['index']
        dest = (self.grid_width - 2, self.grid_height - 1)
        dest_index = self.grid[dest]['index']

        heap = [
            # Distance travelled, current position, visited
            (0, start_index, []),
        ]
        high_score = 0

        while heap:
            score, position, visited = heapq.heappop(heap)
            if position != start_index:
                assert visited

            if position == dest_index:
                ascore = abs(score)
                if ascore > high_score:
                    print(f'New high score of {ascore} beats current {high_score}')
                    high_score = max(ascore, high_score)

                continue

            n = neighbours(self.graph, position, visited)
            for i in n:
                weight = self.graph.edges[position][i]
                heapq.heappush(heap, (score - weight, i, [*visited, position]))

        return high_score

    def run_step_1(self) -> int:
        self.setup(False)
        return self.find_longest_route()

    def run_step_2(self) -> int:
        self.setup(True)
        # 6534
        return self.find_longest_route()


if __name__ == '__main__':
    from aocd import data
    # print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
