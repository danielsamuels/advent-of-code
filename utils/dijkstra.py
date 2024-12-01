# https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/dijkstras-algorithm/
import abc
import pickle
from collections import defaultdict
from queue import PriorityQueue
from typing import Callable

from utils.grid import Position


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [
            [-1 for i in range(num_of_vertices)]
            for j in range(num_of_vertices)
        ]
        self.visited = []

    def add_one_way_edge(self, u: int, v: int, *, weight: int = 1):
        self.edges[u][v] = weight

    def remove_edge(self, u: int, v: int):
        assert self.edges[u][v] != -1
        self.edges[u][v] = -1

    def add_two_way_edge(self, u: int, v: int, weight: int = 1):
        self.edges[u][v] = weight
        self.edges[v][u] = weight


class SparseGraph:
    """Creates a graph which only declares edges when they exist

    Assumes hashes are not accessible, but dots are.
    """
    def __init__(self):
        self.edges = defaultdict(dict)

    def add_one_way_edge(self, source: Position, dest: Position, *, weight: int = 1):
        self.edges[source][dest] = weight

    def add_two_way_edge(self, source: Position, dest: Position, *, weight: int = 1):
        self.add_one_way_edge(source, dest, weight=weight)
        self.add_one_way_edge(dest, source, weight=weight)

    def remove_one_way_edge(self, source: Position, dest: Position):
        self.edges[source].pop(dest, None)

    def remove_two_way_edge(self, source: Position, dest: Position):
        self.remove_one_way_edge(source, dest)
        self.remove_one_way_edge(dest, source)

    def simplify_edges(self):
        # For each point in the graph, if it only has
        # two neighbours (i.e. one in, one out), simplify
        # the path to be e.g. A<->B<->C becomes A<->C
        for source, destinations in tuple(self.edges.items()):
            if len(destinations) != 2:
                continue

            # The weight of A->C is A->B + B->C
            # The weight of C->A is C->B + B->A (which may not be the same)
            destination_keys = list(destinations.keys())
            A = destination_keys[0]
            C = destination_keys[1]
            ac_weight = self.edges[A][source] + self.edges[source][C]
            ca_weight = self.edges[C][source] + self.edges[source][A]

            self.remove_two_way_edge(source, A)
            self.remove_two_way_edge(source, C)

            self.add_one_way_edge(A, C, weight=ac_weight)
            self.add_one_way_edge(C, A, weight=ca_weight)

            break

        # In performing this action, we may have ended up with some more positions
        # with exactly two neighbours, which means we can go through another round.
        # While we're here, also remove any edges which no have no neighbours.
        for source, destinations in self.edges.items():
            if len(destinations) == 2:
                return self.simplify_edges()


def neighbours(graph, current_vertex, visited) -> list[int]:
    return [
        neighbor
        for neighbor in range(graph.v)
        if neighbor not in visited and graph.edges[current_vertex][neighbor] != -1
    ]


def cost_new_lt_old(new_value, old_value) -> bool:
    return new_value < old_value


def dijkstra(graph, start_vertex, cost_fn: Callable = None):
    # print(f'Computing paths from {start_vertex}')
    graph = pickle.loads(pickle.dumps(graph))
    D = {v: float('inf') for v in range(graph.v)}
    D[start_vertex] = 0

    if cost_fn is None:
        cost_fn = cost_new_lt_old

    pq = PriorityQueue()
    pq.put((0, start_vertex))

    while not pq.empty():
        (dist, current_vertex) = pq.get()
        graph.visited.append(current_vertex)

        for neighbor in range(graph.v):
            if graph.edges[current_vertex][neighbor] != -1:
                distance = graph.edges[current_vertex][neighbor]
                if neighbor not in graph.visited:
                    old_cost = D[neighbor]
                    new_cost = D[current_vertex] + distance

                    if cost_fn(new_cost, old_cost):
                        pq.put((new_cost, neighbor))
                        D[neighbor] = new_cost
    return D