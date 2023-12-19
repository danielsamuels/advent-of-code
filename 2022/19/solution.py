import enum
import re
from collections import namedtuple, deque

from aocd import data


class Robot(enum.Enum):
    ORE = enum.auto()
    CLAY = enum.auto()
    OBSIDIAN = enum.auto()
    GEODE = enum.auto()

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
    'time',
    'ore_robots', 'clay_robots', 'obsidian_robots', 'geode_robots',
    'ore', 'clay', 'obsidian', 'geode',
])


class Day:
    def __init__(self, data):
        self.data = data.splitlines()
        self.blueprints = [
            Blueprint._make(map(int, re.findall(r'\d+', row)))
            for row in self.data
        ]

    def simulate(self, blueprint: Blueprint) -> int:
        initial_state = State(0, 1, 0, 0, 0, 0, 0, 0, 0)
        best_score = 0

        max_costs = {
            Material.ORE: max([blueprint.ore_ore, blueprint.clay_ore, blueprint.obsidian_ore, blueprint.geode_ore]),
            Material.CLAY: blueprint.obsidian_clay,
            Material.OBSIDIAN: blueprint.geode_obsidian,
        }

        queue = deque([initial_state])
        while queue:
            state = queue.popleft()
            state = state._replace(time=state.time + 1)

            # What can we afford to buy?
            can_afford = set()
            if state.ore >= blueprint.ore_ore:
                can_afford.add(Robot.ORE)
            if state.ore >= blueprint.clay_ore:
                can_afford.add(Robot.CLAY)
            if state.ore >= blueprint.obsidian_ore and state.clay >= blueprint.obsidian_clay:
                can_afford.add(Robot.OBSIDIAN)
            if state.ore >= blueprint.geode_ore and state.obsidian >= blueprint.geode_obsidian:
                can_afford.add(Robot.GEODE)

            # ...and what would we _want_ to buy?
            if state.ore_robots >= max_costs[Material.ORE]:
                can_afford.discard(Robot.ORE)
            if state.clay_robots >= max_costs[Material.CLAY]:
                can_afford.discard(Robot.CLAY)
            if state.obsidian_robots >= max_costs[Material.OBSIDIAN]:
                can_afford.discard(Robot.OBSIDIAN)

            # Acquire resources
            state = state._replace(
                ore=min(state.ore + state.ore_robots, max_costs[Material.ORE]),
                clay=min(state.clay + state.clay_robots, max_costs[Material.CLAY]),
                obsidian=min(state.obsidian + state.obsidian_robots, max_costs[Material.OBSIDIAN]),
                geode=state.geode + state.geode_robots,
            )

            if state.time == 24:
                # ...and we're done!
                best_score = max(best_score, state.geode)
                continue

            for robot in can_afford:
                # Try all these different options
                if robot == Robot.ORE:
                    queue.append(state._replace(
                        ore_robots=state.ore_robots + 1,
                        ore=state.ore - blueprint.ore_ore,
                    ))
                if robot == Robot.CLAY:
                    queue.append(state._replace(
                        clay_robots=state.clay_robots + 1,
                        ore=state.ore - blueprint.clay_ore,
                    ))
                if robot == Robot.OBSIDIAN:
                    queue.append(state._replace(
                        obsidian_robots=state.obsidian_robots + 1,
                        ore=state.ore - blueprint.obsidian_ore,
                        clay=state.clay - blueprint.obsidian_clay,
                    ))
                if robot == Robot.GEODE:
                    queue.append(state._replace(
                        geode_robots=state.geode_robots + 1,
                        ore=state.ore - blueprint.geode_ore,
                        obsidian=state.obsidian - blueprint.geode_obsidian,
                    ))

            # Also do nothing
            queue.append(state)

        print(f'Blueprint {blueprint.id} scored {best_score}')
        return best_score

    def run_step_1(self) -> int:
        return sum([
            self.simulate(blueprint)
            for blueprint in self.blueprints
        ])



    def run_step_2(self) -> int:
        return 0