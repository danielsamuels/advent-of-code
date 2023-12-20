import enum
import heapq
import math
import re
from collections import namedtuple


class Robot(enum.IntEnum):
    GEODE = 1
    OBSIDIAN = 2
    CLAY = 3
    ORE = 4
    NOTHING = 5


class Material(enum.Enum):
    ORE = enum.auto()
    CLAY = enum.auto()
    OBSIDIAN = enum.auto()


Blueprint = namedtuple('Blueprint', [
    'id',
    'ore_ore',
    'clay_ore',
    'obsidian_ore', 'obsidian_clay',
    'geode_ore', 'geode_obsidian',
])

State = namedtuple('State', [
    'time', 'theoretical_geodes',
    'ore_robots', 'clay_robots', 'obsidian_robots', 'geode_robots',
    'ore', 'clay', 'obsidian', 'geode',
    'purchase',
    'history',
])


class Day:
    def __init__(self, data):
        self.data = data.splitlines()
        self.blueprints = [
            Blueprint._make(map(int, re.findall(r'\d+', row)))
            for row in self.data
        ]

    def simulate(self, blueprint: Blueprint, time_limit: int) -> int:
        initial_state = State(0, 0, 1, 0, 0, 0, 0, 0, 0, 0, None, [])
        best_score = 0
        time_limit = -time_limit

        max_costs = {
            Material.ORE: max([blueprint.ore_ore, blueprint.clay_ore, blueprint.obsidian_ore, blueprint.geode_ore]),
            Material.CLAY: blueprint.obsidian_clay,
            Material.OBSIDIAN: blueprint.geode_obsidian,
        }

        heap = [initial_state]
        while heap:
            state = heapq.heappop(heap)

            if not state.purchase:
                # Choose which robot we want to build next.
                # Based on the robots we've currently got, what are viable purchases?
                viable_robots = set()

                if state.ore_robots < max_costs[Material.ORE]:
                    viable_robots.add(Robot.ORE)

                if state.clay_robots < max_costs[Material.CLAY]:
                    viable_robots.add(Robot.CLAY)

                if state.clay_robots and state.obsidian_robots < max_costs[Material.OBSIDIAN]:
                    viable_robots.add(Robot.OBSIDIAN)

                if state.obsidian_robots:
                    viable_robots.add(Robot.GEODE)

                for robot in viable_robots:
                    # We'll work towards each one
                    # How many iterations will it take to get there?
                    heapq.heappush(heap, state._replace(
                        purchase=robot,
                    ))

                continue

            # We go backwards in time, rather than forwards
            # to allow Python's min heap to work as expected
            state = state._replace(time=state.time - 1)
            time_left = abs(time_limit - state.time)

            # If we could build _nothing_ but geode robots for the remaining time,
            # would we beat the current max score?
            m = time_left + state.geode_robots
            theoretical_geodes = state.geode + ((m - 1) / 2 + 1) * (m - 1 + 1)
            state = state._replace(
                theoretical_geodes=theoretical_geodes,
            )
            if theoretical_geodes <= best_score:
                continue

            # Can we afford to make the purchase yet?
            can_afford = True
            if state.purchase == Robot.ORE and state.ore >= blueprint.ore_ore:
                state = state._replace(
                    ore=state.ore - blueprint.ore_ore,
                )
            elif state.purchase == Robot.CLAY and state.ore >= blueprint.clay_ore:
                state = state._replace(
                    ore=state.ore - blueprint.clay_ore,
                )
            elif state.purchase == Robot.OBSIDIAN and state.ore >= blueprint.obsidian_ore and state.clay >= blueprint.obsidian_clay:
                state = state._replace(
                    ore=state.ore - blueprint.obsidian_ore,
                    clay=state.clay - blueprint.obsidian_clay,
                )
            elif state.purchase == Robot.GEODE and state.ore >= blueprint.geode_ore and state.obsidian >= blueprint.geode_obsidian:
                state = state._replace(
                    ore=state.ore - blueprint.geode_ore,
                    obsidian=state.obsidian - blueprint.geode_obsidian,
                )
            else:
                state = state._replace(
                    history=state.history + [f'{abs(state.time)}: Cannot afford {state.purchase.name}'],
                )
                can_afford = False

            # Acquire resources
            state = state._replace(
                ore=state.ore + state.ore_robots,
                clay=state.clay + state.clay_robots,
                obsidian=state.obsidian + state.obsidian_robots,
                geode=state.geode + state.geode_robots,
            )

            # Complete the building of new purchase, if any
            if can_afford:
                state = state._replace(
                    history=state.history + [f'{abs(state.time)}: Buying {state.purchase.name}'],
                )

                if state.purchase == Robot.ORE:
                    state = state._replace(
                        ore_robots=state.ore_robots + 1,
                    )
                if state.purchase == Robot.CLAY:
                    state = state._replace(
                        clay_robots=state.clay_robots + 1,
                    )
                if state.purchase == Robot.OBSIDIAN:
                    state = state._replace(
                        obsidian_robots=state.obsidian_robots + 1,
                    )
                if state.purchase == Robot.GEODE:
                    state = state._replace(
                        geode_robots=state.geode_robots + 1,
                    )

                state = state._replace(
                    purchase=None,
                )

            if time_left == 0:
                # ...and we're done!
                if state.geode > best_score:
                    best_score = max(best_score, state.geode)
                    # print(f'Blueprint {blueprint.id}, new high score is {state.geode}')
                    # print('\n'.join(state.history))
                    # print()

                continue

            heapq.heappush(heap, state)

        # print(f'Blueprint {blueprint.id} scored {best_score}')
        return best_score

    def run_step_1(self) -> int:
        return sum([
            blueprint.id * self.simulate(blueprint, 24)
            for blueprint in self.blueprints
        ])

    def run_step_2(self) -> int:
        return math.prod([
            self.simulate(blueprint, 32)
            for blueprint in self.blueprints[:3]
        ])