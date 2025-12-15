from functools import cache
from pprint import pprint
from typing import TypeVar, Any, cast, Generator
from collections.abc import Callable

from black.comments import lru_cache
from frozendict import frozendict
from tqdm import tqdm

T = TypeVar("T")


def find_all_paths(
    graph: dict[T, Any],
    start: T,
    end: T,
    test_fn: Callable[[tuple[T, ...]], bool] = lambda path: True,
) -> list[tuple[T, ...]]:
    """
    For this current path, return all sub-paths until we reach `end_state`.

    For a graph of the following structure:
        a: b c
        b: d
        c: d e
        d: out
        e: f
        f: out
    ...and a starting path of ('a',),

    We should get a result of:
        [
            ('a', 'b', 'd', 'out'),
            ('a', 'c', 'd', 'out'),
            ('a', 'c', 'e', 'f', 'out'),
        ]
    """

    @lru_cache(maxsize=256)
    def downstream_nodes(node: T) -> list[tuple[T, ...]]:
        if node == end:
            return [(node,)]

        suffixes = []
        for sub_node in graph.get(node, []):
            for suffix in downstream_nodes(sub_node):
                new_path = (node,) + suffix
                if suffix == end:
                    if test_fn(new_path):
                        print(f"Found a viable path: {new_path=}")
                        suffixes.append(new_path)
                else:
                    suffixes.append(new_path)

        return suffixes

    return downstream_nodes(start)
