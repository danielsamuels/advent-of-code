import collections
import dataclasses

FREE_SPACE = -1


@dataclasses.dataclass
class File:
    index: int
    size: int

    def __repr__(self):
        if self.index == FREE_SPACE:
            return f'.' * self.size
        return f'{self.index}' * self.size


class Day:
    def __init__(self, data: str):
        p1_disk: list[File] = []
        p2_disk: list[File] = []

        file_index = 0

        for index, value in enumerate(map(int, data)):
            if index % 2 == 0:
                # This is a file
                p1_disk.extend([File(file_index, 1) for _ in range(value)])
                p2_disk.append(File(file_index, value))
                file_index += 1
            else:
                # This is free space
                p1_disk.extend([FREE_SPACE] * value)
                p2_disk.append(File(FREE_SPACE, value))


        self.p1_disk = p1_disk
        self.p2_disk = p2_disk

    def defrag(self) -> list:
        # Operate on a copy to make it safe to run both parts
        disk = list(self.p1_disk)

        # Get the indexes of all the free space
        free_indexes = [i for i, val in enumerate(disk) if val == FREE_SPACE]
        all_values = collections.deque([val for val in disk if val != FREE_SPACE])

        # Construct a new disk
        new_disk = []
        for x in range(len(disk)):
            if all_values:
                if x in free_indexes:
                    new_disk.append(all_values.pop())
                else:
                    new_disk.append(all_values.popleft())
            else:
                new_disk.extend([FREE_SPACE] * len(free_indexes))
                break

        return new_disk

    def move_files(self) -> list:
        disk = list(self.p2_disk)
        available_files = collections.deque([
            file for file in disk if file.index != FREE_SPACE
        ])

        while available_files:
            candidate = available_files.pop()
            candidate_index = disk.index(candidate)

            # Go through the free spaces and see if this would fit
            for file_index, file in enumerate(disk):
                if file.index == FREE_SPACE and candidate.size <= file.size and file_index < candidate_index:
                    # There's a space for this file
                    disk[candidate_index], disk[file_index] = disk[file_index], disk[candidate_index]
                    # If the candidate was smaller, pad after the candidate and adjust the space size
                    size_diff = file.size - candidate.size
                    if size_diff:
                        disk.insert(file_index + 1, File(FREE_SPACE, size_diff))
                        file.size = candidate.size
                    break

        return disk

    def run_step_1(self) -> int:
        disk = self.defrag()
        return sum(index * item.index for index, item in enumerate(disk) if item is not FREE_SPACE)

    def run_step_2(self) -> int:
        disk = self.move_files()
        # An item of size 4 at position 2 should be 2+(3+4+5)
        result = 0
        global_index = 0
        for file in disk:
            if file.index != FREE_SPACE:
                for x in range(file.size):
                    result += file.index * (global_index + x)

            global_index += file.size

            # result += sum((index + x) * file.index for x in range(file.size))
            # print(index, file)

        return result
        # return sum(((index + item.size) * 2) * item.index for index, item in enumerate(disk) if item is not FREE_SPACE)


if __name__ == '__main__':
    from aocd import data

    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
