Position = tuple[int, int]
Positions = list[Position]
PositionHistory = list[Positions]


def move_head(head: Position, direction: str) -> Position:
    # Get the current position and apply the movement to the head.
    head_x, head_y = head
    return (
        head_x + (1 if direction == 'R' else -1 if direction == 'L' else 0),
        head_y + (1 if direction == 'D' else -1 if direction == 'U' else 0)
    )


def move_tail(head: Position, tail: Position) -> Position:
    # Get the current position and apply the movement to the head.
    [head_x, head_y], [tail_x, tail_y] = head, tail
    # What is the distance from the head to the tail?
    dist_x, dist_y = head_x - tail_x, head_y - tail_y

    # The tail has fallen behind, catch up
    if max(abs(dist_x), abs(dist_y)) == 2:
        if dist_x != 0:
            tail_x += dist_x // abs(dist_x)
        if dist_y != 0:
            tail_y += dist_y // abs(dist_y)

        tail = (tail_x, tail_y)

    return tail


def run_simulation(data: str, knots: int) -> PositionHistory:
    positions: PositionHistory = [
        [(0, 0) for _ in range(knots)]
    ]
    for command in data.split('\n'):
        direction, num = command.split(' ')
        for iteration in range(int(num)):
            latest_position = [*positions[-1]]

            # Move the head first
            latest_position[0] = move_head(latest_position[0], direction)

            # Next move the knots
            for point in range(1, knots):
                latest_position[point] = move_tail(
                    latest_position[point - 1],
                    latest_position[point],
                )

            positions.append(latest_position)

    return positions


def run_step_1(data: str) -> int:
    positions = run_simulation(data, 2)
    return len(set(p[-1] for p in positions))


def run_step_2(data: str) -> int:
    positions = run_simulation(data, 10)
    return len(set(p[-1] for p in positions))


if __name__ == "__main__":
    with open(f'data/day_9.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)
