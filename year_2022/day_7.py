from collections import defaultdict
from pathlib import Path

FS = dict[Path, int]


def construct_filesystem(data: str) -> FS:
    """Read each command, and any results and build a picture of the disk"""
    layout = defaultdict(int)
    current_directory = Path('/')

    for row in data.split('\n'):
        ignored_lines = [
            '$ cd /',
            '$ ls',
        ]
        if row in ignored_lines:
            continue

        if row.startswith('$ cd'):
            _, _, path = row.split(' ')
            if path == '..':
                current_directory = current_directory.parent
            else:
                current_directory = current_directory / path
        else:
            attr, name = row.split(' ')
            if attr != 'dir':
                # Add the filesize to this dir and all parent dirs
                layout[current_directory] += int(attr)
                for parent in current_directory.parents:
                    layout[parent] += int(attr)

    return layout


def run_step_1(data: str) -> int:
    fs = construct_filesystem(data)
    # Get directories with a total size of <=100000 and sum them
    return sum([
        size for size in fs.values()
        if size <= 100_000
    ])


def run_step_2(data: str) -> int:
    fs = construct_filesystem(data)

    total_space = 70_000_000
    used_space = fs[Path('/')]
    free_space = total_space - used_space
    required_deletion = 30_000_000 - free_space

    return min([
        size for size in fs.values()
        if size >= required_deletion
    ])


if __name__ == "__main__":
    with open(f'data/day_7.txt', 'r') as f:
        read_data = f.read()

    result = run_step_1(read_data)
    print(result)

    result_2 = run_step_2(read_data)
    print(result_2)
