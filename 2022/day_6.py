def find_marker(buffer: str, size: int) -> int:
    for offset in range(len(buffer) - size - 1):
        subset = buffer[offset:offset + size]
        if len(set(subset)) == size:
            return offset + size


def run_step_1(data: str) -> int:
    return find_marker(data, 4)


def run_step_2(data: str) -> int:
    return find_marker(data, 14)


if __name__ == "__main__":
    with open(f'data/day_6.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)