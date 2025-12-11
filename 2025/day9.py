import itertools
from operator import itemgetter
from pprint import pprint
from typing import cast
from aocd import data, submit

from utils.grid import (
    FloodFill,
    Position,
    bridge_points,
    flood_fill,
    flood_fill_dict,
    form_square,
    grid_bounds,
    print_grid,
    print_sparse_grid, compress_positions,
)
from utils.polygon import Polygon

test_data = """
7,1
11,1
11,7
9,7
9,5
2,5
2,3
7,3
""".strip()

TESTING = False
if TESTING:
    data = test_data


def part_1() -> None:
    positions: list[Position] = [
        cast(Position, tuple(map(int, p)))
        for row in data.splitlines()
        if (p := row.split(","))
    ]
    combos = itertools.combinations(positions, 2)

    result = max(
        [
            (abs(ax - bx) + 1) * (abs(ay - by) + 1)
            for a, b in combos
            if (ax := a[0]) and (ay := a[1]) and (bx := b[0]) and (by := b[1])
        ]
    )

    print(f"{result=}")
    if not TESTING:
        submit(result, part="a")


def part_2() -> None:
    result = 0

    positions: list[Position] = [
        cast(Position, tuple(map(int, p)))
        for row in data.splitlines()
        if (p := row.split(","))
    ]
    # To help the border be completed later, duplicate the first co-ordinate
    positions.append(positions[0])

    positions, x_map, y_map, inv_x, inv_y, w, h = compress_positions(positions)

    # 3) Use compressed_positions for building the grid and flood-fill:
    #    - when bridging edges, call bridge_points on compressed coordinates
    #    - run flood_fill_dict on the compressed grid of size (w, h)
    # 4) When computing the original area for a candidate pair (a, b) use inverse maps:
    #    orig_ax, orig_ay = inv_x[a[0]], inv_y[a[1]]
    #    orig_bx, orig_by = inv_x[b[0]], inv_y[b[1]]
    #    size = (abs(orig_ax - orig_bx) + 1) * (abs(orig_ay - orig_by) + 1)


    # Build the edges of the grid by bridging pairs of positions
    print("Building base grid")
    grid: dict[Position, str] = dict()
    combos = itertools.pairwise(positions)

    for a, b in combos:
        grid[a] = "#"
        grid[b] = "#"
        for pos in bridge_points(a, b):
            grid[pos] = "X"

    # print("How I think the grid looks:")
    # print_sparse_grid(grid)

    # Next, determine the inner positions of the grid by flood
    # filling the outside, then subtracting those places from
    # the overall space.
    print("\nDetermining negative space")
    *_, (grid_width, grid_height) = grid_bounds(grid)
    filled = flood_fill_dict(grid, FloodFill.REACHED, width=w, height=h)
    assert len(filled) > 0

    print(f"\nFlood fill complete ({len(filled)} filled), filling in space")
    for row in range(grid_height):
        for col in range(grid_width):
            position: Position = (col, row)
            grid_val = grid.get(position)
            if position in filled or grid_val:
                continue

            # Make this green
            grid[position] = "X"

    # print_sparse_grid(grid)

    # Now we can apply the same logic as seen in part 1
    # to determine the candidate squares
    # 4) When computing the original area for a candidate pair (a, b) use inverse maps:
    #    orig_ax, orig_ay = inv_x[a[0]], inv_y[a[1]]
    #    orig_bx, orig_by = inv_x[b[0]], inv_y[b[1]]
    #    size = (abs(orig_ax - orig_bx) + 1) * (abs(orig_ay - orig_by) + 1)
    print("\nDetermining candidate squares")
    combos = itertools.combinations(positions, 2)
    squares = sorted(
        [
            (a, b, (abs(ax - bx) + 1) * (abs(ay - by) + 1))
            for a, b in combos
            if (ax := inv_x[a[0]]) and (ay := inv_y[a[1]]) and (bx := inv_x[b[0]]) and (by := inv_y[b[1]])
        ],
        key=itemgetter(2),
        reverse=True,
    )

    # Now that we have our list of squares, largest first,
    # go through each in turn and determine their eligibility
    print("\nDetermining square eligibility")
    for a, b, size in squares:
        points = form_square(a, b)
        point_values = {p: grid.get(p) for p in points}
        point_value_set = set(point_values.values())

        if None not in point_value_set:
            result = size
            break

    print(f"{result=}")
    if not TESTING:
        submit(result, part="b")


if __name__ == "__main__":
    # part_1()
    part_2()
