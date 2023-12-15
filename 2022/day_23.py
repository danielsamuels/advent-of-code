import copy
from collections import defaultdict, deque

from utils.grid import parse_grid, Direction, relative_points_occupied, compute_new_position, print_grid, grid_bounds, \
    dict_grid_to_list


class Day:
    def __init__(self, data: str):
        self.grid = parse_grid(data)
        self.directions = deque([Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST])

    def simulate_rounds(self, rounds: int) -> int | None:
        # print('\n== Starting position ==')
        elf_count = len(self.grid)
        # print_grid(dict_grid_to_list(self.grid), borders=False)
        # print()

        all_directions = list(Direction)
        proposals = {
            Direction.NORTH: [Direction.NORTHWEST, Direction.NORTH, Direction.NORTHEAST],
            Direction.SOUTH: [Direction.SOUTHWEST, Direction.SOUTH, Direction.SOUTHEAST],
            Direction.WEST: [Direction.NORTHWEST, Direction.WEST, Direction.SOUTHWEST],
            Direction.EAST: [Direction.NORTHEAST, Direction.EAST, Direction.SOUTHEAST],
        }

        for round_ in range(1, rounds + 1):
            # print(f'== Round {round_} ==')
            elves = copy.deepcopy(self.grid)
            assert len(elves) == elf_count
            new_elves = {}

            """
            During the first half of each round, each Elf considers the eight positions adjacent to themself.
            If no other Elves are in one of those eight positions, the Elf does not do anything during this round.
            """
            all_elves_free = True
            for location, v in elves.items():
                if not any(relative_points_occupied(self.grid, location, all_directions)):
                    new_elves[location] = 1
                else:
                    all_elves_free = False

            if all_elves_free:
                print('All elves find themselves with space.')
                # print_grid(dict_grid_to_list(self.grid), borders=False)
                # print()
                return round_

            """
            Otherwise, the Elf looks in each of four directions in the following order
            and proposes moving one step in the first valid direction:
            - If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
            - If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
            - If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
            - If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
            """
            proposed_locations = defaultdict(list)
            for elf in elves:
                done = False

                if elf in new_elves:
                    continue

                for direction in self.directions:
                    # print(f'Elf {elf} thinking about {direction.name}..')
                    positions = proposals[direction]
                    if not any(relative_points_occupied(self.grid, elf, positions)):
                        # print(f'- Elf wants to move {direction.name}')
                        proposed_locations[compute_new_position(elf, direction)].append(elf)
                        done = True
                        break

                if not done:
                    new_elves[elf] = 1

            """
            After each Elf has had a chance to propose a move, the second half of the round can begin.
            Simultaneously, each Elf moves to their proposed destination tile if they were the only Elf to propose moving to that position.
            If two or more Elves propose moving to the same position, none of those Elves move.
            """
            for prop_loc, prop_elves in proposed_locations.items():
                if len(prop_elves) == 1:
                    new_elves[prop_loc] = 1
                else:
                    for prop_elf in prop_elves:
                        new_elves[prop_elf] = 1

            """
            Finally, at the end of the round, the first direction the Elves considered is moved to the end of the list of directions.
    
            For example, during the second round, the Elves would try proposing a move to the south first, then west, then east, then north.
            On the third round, the Elves would first consider west, then east, then north, then south.
            """
            assert len(new_elves) == elf_count
            self.grid = new_elves
            self.directions.rotate(-1)

            # print_grid(dict_grid_to_list(self.grid), borders=False)
            # print()

    @property
    def step_1_score(self):
        tl, tr, bl, br = grid_bounds(self.grid)
        width, height = br[0] - tl[0] + 1, br[1] - tl[1] + 1
        return (width * height) - len(self.grid)

    def run_step_1(self) -> int:
        self.simulate_rounds(10)
        return self.step_1_score

    def run_step_2(self) -> int:
        return self.simulate_rounds(1000)


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    result = Day(read_data).run_step_1()
    print(f'Step 1: {result}')

    result_2 = Day(read_data).run_step_2()
    print(f'Step 2: {result_2}')
