# https://stackabuse.com/courses/graphs-in-python-theory-and-implementation/lessons/dijkstras-algorithm/
import pickle
from queue import PriorityQueue
from typing import Callable


class Graph:
    def __init__(self, num_of_vertices):
        self.v = num_of_vertices
        self.edges = [[-1 for i in range(num_of_vertices)] for j in range(num_of_vertices)]
        self.visited = []

    def add_one_way_edge(self, u: int, v: int, *, weight: int = 1):
        self.edges[u][v] = weight

    def remove_edge(self, u: int, v: int):
        assert self.edges[u][v] != -1
        self.edges[u][v] = -1

    def add_two_way_edge(self, u: int, v: int, weight: int = 1):
        self.edges[u][v] = weight
        self.edges[v][u] = weight


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