def run_cycles(data: str) -> tuple[dict[int], list[str]]:
    commands = data.split('\n')
    cycle = 0
    cycles = {}
    stack = []
    x = 1
    crt = ['.'] * 241

    while commands or stack:
        cycle += 1
        cycles[cycle] = {
            'x': x,
            'strength': x * cycle,
        }

        # Determine the CRT pixel behaviour
        sprite_position = [x % 40, (x + 1) % 40, (x + 2) % 40]
        row_pos = cycle % 40
        if row_pos in sprite_position:
            crt[cycle] = '#'

        # Is there anything on the stack?
        if stack:
            x += stack.pop()
        else:
            command = commands.pop(0)
            match command.strip().split():
                case ['addx', num]:
                    stack.append(int(num))

    return cycles, crt[1:]


def build_crt(crt: list[str]):
    return '\n'.join([
        ''.join(crt[0:40]),
        ''.join(crt[40:80]),
        ''.join(crt[80:120]),
        ''.join(crt[120:160]),
        ''.join(crt[160:200]),
        ''.join(crt[200:240]),
    ])


def run_steps(data: str) -> int:
    cycles, crt = run_cycles(data)

    # Step 2 output
    print(build_crt(crt))

    targets = [20, 60, 100, 140, 180, 220]
    return sum([
        cycles[x]['strength']
        for x in targets
    ])


if __name__ == "__main__":
    with open(f'data/day_10.txt', 'r') as f:
        read_data = f.read()

    step_1_result = run_steps(read_data)
    print(step_1_result)
