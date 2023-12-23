import dataclasses
import itertools
import operator
import os
import string
from functools import cached_property, cache
from typing import Self

from tqdm import tqdm

Position3D = tuple[int, int, int]


@dataclasses.dataclass(kw_only=True)
class Brick:
    day: 'Day'
    start: Position3D
    end: Position3D
    label: int

    @property
    def points(self):
        return [
            (x, y, z)
            for x in range(self.start[0], self.end[0] + 1)
            for y in range(self.start[1], self.end[1] + 1)
            for z in range(self.start[2], self.end[2] + 1)
        ]

    def __repr__(self):
        return f'{self.label}{{{self.points[0]}-{self.points[-1]}}}'

    @property
    def supporting(self) -> list[Self]:
        """What is directly above this brick?"""
        if g := self.day.graph.get(self.label):
            return g['supporting']

        return [
            brick
            for brick in self.day.bricks
            if brick is not self and brick.is_supported_by(self)
        ]

    @property
    def supported_by(self) -> list[Self]:
        if g := self.day.graph.get(self.label):
            return g['supported_by']

        return [
            brick
            for brick in self.day.bricks
            if brick is not self and self.is_supported_by(brick)
        ]

    def is_supported_by(self, other: 'Brick') -> bool:
        """Is this supported by that?"""
        return bool(set(self.points_under) & set(other.points))

    @property
    def lowest_z(self):
        return min(self.start[2], self.end[2])

    @property
    def points_under(self) -> list[Position3D]:
        if self.lowest_z <= 1:
            # We're sitting on the bottom, nothing can be underneath
            return []

        return [
            (x, y, z-1)
            for x, y, z in self.points
            if z == self.lowest_z
        ]

    def lowest_point_available(self) -> tuple[Position3D, Position3D]:
        # How low can we go before we hit something?
        points_to_adjust = [
            p for p in self.points
            if p[2] == self.lowest_z
        ]
        lower_by = 0
        for possible_z in range(self.lowest_z - 1, 0, -1):
            # What would the new position be?
            points = [
                (x, y, possible_z)
                for x, y, z in points_to_adjust
            ]
            available = all(
                point not in self.day.grid()
                for point in points
            )
            if available:
                lower_by += 1
                continue

            break

        sx, sy, sz = self.start
        ex, ey, ez = self.end
        return (sx, sy, sz - lower_by), (ex, ey, ez - lower_by)

    @property
    def can_move_down(self) -> bool:
        if self.points_under:
            return all(point not in self.day.grid() for point in self.points_under)
        return False

    def settle(self):
        self.start, self.end = self.lowest_point_available()
        assert not self.can_move_down
        # while self.can_move_down:
        #     print(f'At {self}, and can move down')
        #     self.move_down()

        self.day.clear_grid_cache()
        # print(f'New: {self.start},{self.end}')
        # print(f'Simulated: {start},{end}')

    def move_down(self):
        self.start = self.start[:2] + (self.start[2] - 1,)
        self.end = self.end[:2] + (self.end[2] - 1,)

    @property
    def can_be_disintegrated(self) -> bool:
        # Which bricks does it support?
        # Is each of those bricks supported by anything else?
        for b in self.day.graph[self.label]['supporting']:
            by = self.day.graph[b.label]['supported_by']
            if not len(by) > 1:
                return False

        return True

    def sup_set(self) -> set:
        supporting = self.day.graph[self.label]['supporting']
        result = set(s.label for s in supporting)
        for s in supporting:
            result |= s.sup_set()
        return result

    @property
    def disintegration_result(self):
        if self.can_be_disintegrated:
            return 0

        return len(self.sup_set())

        aff = self.sup_set()
        affected_bricks = set(s.label for s in self.supporting)
        supporting_len = len(self.supporting)
        supporting_scores = [s.disintegration_result for s in self.supporting]

        print(f'{chr(int(self.label) + 65)}: {supporting_len} + {supporting_scores}, {aff}')
        return supporting_len + sum(supporting_scores)


class Day:
    grid: None
    graph: dict = {}

    def __init__(self, data: str):
        self.data = data.splitlines()
        bricks = [
            (tuple(map(int, s.split(','))), tuple(map(int, e.split(','))))
            for s, e in (line.split('~') for line in self.data)
        ]
        self.bricks = self.elongate_bricks(bricks)
        self.settle_bricks()
        self.graph = self.build_brick_graph()

    def elongate_bricks(self, bricks) -> list[Brick]:
        return [
            Brick(
                day=self,
                start=start,
                end=end,
                label=index,
            )
            for index, (start, end) in enumerate(bricks)
        ]

    @cache
    def grid(self) -> dict[Position3D, Brick]:
        result = {}
        for brick in self.bricks:
            for position in brick.points:
                result[position] = brick

        return result

    def clear_grid_cache(self):
        self.grid.cache_clear()

    def settle_bricks(self):
        sorted_bricks = sorted(self.bricks, key=operator.attrgetter('lowest_z'))
        for brick in tqdm(sorted_bricks, desc='Settle bricks', disable='PYTEST_CURRENT_TEST' in os.environ):
            brick.settle()
            
    def build_brick_graph(self):
        return {
            brick.label: {
                'supporting': brick.supporting,
                'supported_by': brick.supported_by,
            }
            for brick in self.bricks
        }

    def run_step_1(self) -> int:


        # Immediately remove any bricks which are single supports of other bricks
        ignore = set()
        for brick in tqdm(self.bricks, desc='Brick checks', disable='PYTEST_CURRENT_TEST' in os.environ):
            supports = brick.supported_by
            if len(supports) == 1:
                ignore.add(supports[0].label)

        to_check = set(b.label for b in self.bricks) - ignore

        # return 0
        return len([
            1
            for i in tqdm(to_check, desc='Disintegrations', disable='PYTEST_CURRENT_TEST' in os.environ)
            if self.bricks[i].can_be_disintegrated
        ])

    def run_step_2(self) -> int:
        # 751 is too low
        # 138660 is too high
        result = sum([
            brick.disintegration_result
            for brick in tqdm(self.bricks, desc='Results', disable='PYTEST_CURRENT_TEST' in os.environ)
        ])

        if 'PYTEST_CURRENT_TEST' not in os.environ:
            assert result > 751
            assert result < 138660
        return result


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
