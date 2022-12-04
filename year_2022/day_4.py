def parse_range(value: str) -> set[int]:
    start, end = map(int, value.split('-'))
    return set(range(start, end + 1))


def convert_pairs_to_ranges(pair: str) -> tuple[set[str]]:
    elf_1, elf_2 = pair.split(',')
    return parse_range(elf_1), parse_range(elf_2)


def full_intercepts(pairs: tuple[set[str]]):
    p1, p2 = pairs
    return p1 < p2 or p1 > p2 or p1 == p2


def run_step_1(data: str) -> int:
    pairs = data.split('\n')
    ranges = map(convert_pairs_to_ranges, pairs)
    fully_contained_ranges = list(filter(full_intercepts, ranges))
    return len(fully_contained_ranges)


def partial_intercepts(pairs: tuple[set[str]]):
    p1, p2 = pairs
    return len(p1 & p2) > 0


def run_step_2(data: str) -> int:
    pairs = data.split('\n')
    ranges = map(convert_pairs_to_ranges, pairs)
    partially_contained_ranges = list(filter(partial_intercepts, ranges))
    return len(partially_contained_ranges)


if __name__ == "__main__":
    with open(f'data/day_4.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)