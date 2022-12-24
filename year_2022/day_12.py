import itertools
import operator
import string
from multiprocessing import Pool

from utils.dijkstra import Graph, dijkstra
from utils.grid import Direction

Position = tuple[int, int]
Heightmap = list[list[int]]

letters = string.ascii_lowercase + string.ascii_uppercase
a = letters.index('a')
z = letters.index('z')
S = letters.index('S')
E = letters.index('E')


def parse_input(data: str) -> tuple[Heightmap, Position, Position]:
    # Return the heightmap, the starting point and the target location(s)
    starting_point: Position = (0, 0)
    target_point: Position = (0, 0)
    heightmap = [
        list(map(lambda l: letters.index(l), row))
        for row in data.splitlines()
    ]
    # Find the starting point
    for y, row in enumerate(heightmap):
        for x, x_val in enumerate(row):
            if x_val == S:
                print(f'Found start at {x},{y}')
                starting_point = (x, y)
                heightmap[y][x] = 0
            if x_val == E:
                print(f'Found target at {x},{y}')
                target_point = (x, y)
                heightmap[y][x] = z

    return heightmap, starting_point, target_point


def available_directions(heightmap, position: Position) -> set[Direction]:
    width, height = len(heightmap[0]), len(heightmap)
    x, y = position
    current_value = heightmap[y][x]
    max_value = current_value + 1
    directions = set()

    # Can go up?
    if y > 0 and heightmap[y - 1][x] <= max_value:
        directions.add(Direction.NORTH)
    # Can go down?
    # If 5x5, y must be < 4 [0, 1, 2, 3, 4]
    if y < height - 1 and heightmap[y + 1][x] <= max_value:
        directions.add(Direction.SOUTH)

    # Can go left?
    if x > 0 and heightmap[y][x - 1] <= max_value:
        directions.add(Direction.WEST)

    # Can go right?
    if x < width - 1 and heightmap[y][x + 1] <= max_value:
        directions.add(Direction.EAST)

    return directions


def all_available_directions(heightmap) -> dict[Position, set[Direction]]:
    dimensions = (len(heightmap[0]), len(heightmap))
    return {
        (x, y): available_directions(heightmap, (x, y))
        for x, y in itertools.product(range(dimensions[0]), range(dimensions[1]))
    }


def node_index(heightmap, position: Position) -> int:
    # For a 4x4 grid:
    # 0 1 2 3
    # 4 5 6 7
    # ...
    # (0, 0) -> 0
    # (1, 0) -> 1
    # (0, 1) -> 4
    # (1, 1) -> 5

    x, y = position
    width, height = len(heightmap[0]), len(heightmap)
    return (y * width) + (x % width)


def build_graph(heightmap) -> Graph:
    all_nodes = all_available_directions(heightmap)

    g = Graph(len(all_nodes))
    for node, directions in all_nodes.items():
        for direction in directions:
            target = move(node, direction)
            g.add_one_way_edge(
                node_index(heightmap, node),
                node_index(heightmap, target),
                1,
            )

    return g


def flatten_routes(source, output: list = None):
    top_level = False
    if output is None:
        top_level = True
        output = []

    # Take deeply nested lists of lists and flatten them to a single list of lists
    for item in source:
        if item and isinstance(item[0], tuple):
            # Found an actual route!
            output.append(item)
        else:
            output = flatten_routes(item, output)

    return output


def move(current_position: Position, target_direction: Direction) -> Position:
    return tuple(map(operator.add, current_position, target_direction.value))


def plot_routes(heightmap, starting_point, target_point) -> list[str]:
    s_x, s_y = starting_point
    t_x, t_y = target_point

    # For each point, determine which directions are available
    position_directions = all_available_directions(heightmap)
    valid_routes = []

    def plot_route(route, new_position):
        route = route + [new_position]

        # If the route we're working on is already longer than the shortest
        # existing route, then don't bother continuing.
        if valid_routes and len(route) > min(len(r) for r in valid_routes):
            return

        if new_position == target_point:
            print(f'Found valid route of length {len(route)}: {route}')
            valid_routes.append(route)
            return

        directions = position_directions[new_position]
        if not directions or all(d in route for d in directions):
            # This route didn't make it to the target, don't return anything
            return

        for direction in directions:
            if move(new_position, direction) not in route:
                plot_route(route, move(new_position, direction))

    # Starting at the start, plot the available routes
    plot_route([], starting_point)
    return valid_routes


def run_step_1(data: str) -> int:
    heightmap, starting_point, target_point = parse_input(data)
    starting_point_index = node_index(heightmap, starting_point)
    target_point_index = node_index(heightmap, target_point)

    graph = build_graph(heightmap)
    routes = dijkstra(graph, starting_point_index)
    return routes[target_point_index]


def distance(graph, target_point_index, starting_point):
    return dijkstra(graph, starting_point)[target_point_index]


def run_step_2(data: str) -> int:
    heightmap, _, target_point = parse_input(data)
    target_point_index = node_index(heightmap, target_point)

    # Get all points of height 0
    width, height = len(heightmap[0]), len(heightmap)
    starting_points = [
        node_index(heightmap, (x, y))
        for x, y in itertools.product(range(width), range(height))
        if heightmap[y][x] == 0
    ]
    print(f'{len(starting_points)} starting points: {starting_points}')

    graph = build_graph(heightmap)

    with Pool() as p:
        lengths = p.starmap(distance, (
            [graph, target_point_index, starting_point]
            for starting_point in starting_points
        ))

    return min(lengths)


if __name__ == "__main__":
    with open(f'data/day_11.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)
