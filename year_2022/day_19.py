import os
import random
import re
from multiprocessing import Pool
from typing import Union

from tqdm import trange

Material = Union['geode', 'obsidian', 'clay', 'ore']
materials: list[Material] = ['geode', 'obsidian', 'clay', 'ore']


class Blueprint:
    robot_costs: dict[Material, dict[Material, int]]
    robot_inventory: dict[Material, dict[str, int]]
    material_inventory: dict[Material, int]

    def __init__(self, definition: str):
        results = list(map(int, re.findall(r'(\d+)', definition)))
        self.robot_costs = {
            'ore': {'ore': results[1]},
            'clay': {'ore': results[2]},
            'obsidian': {'ore': results[3], 'clay': results[4]},
            'geode': {'ore': results[5], 'obsidian': results[6]}
        }
        self.robot_inventory = {
            'ore': {'own': 1, 'pending': 0},
            'clay': {'own': 0, 'pending': 0},
            'obsidian': {'own': 0, 'pending': 0},
            'geode': {'own': 0, 'pending': 0},
        }
        self.material_inventory = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}

    def can_afford(self, material: Material) -> bool:
        return all([
            self.material_inventory[material] >= amount
            for material, amount in self.robot_costs[material].items()
        ])

    @property
    def affordable_robots(self) -> list[Material]:
        return [
            material
            for material in materials
            if self.can_afford(material)
        ]

    def distance_to(self, material: Material):
        print()


class Day:
    def __init__(self, data: str):
        self.blueprints = [
            Blueprint(line)
            for line in data.splitlines()
        ]
        self.materials: list[Material] = ['geode', 'obsidian', 'clay', 'ore']  # This is also the purchase priority

    @staticmethod
    def can_afford(need: dict[str, int], have: dict[str, int]):
        return all([
            have[need_key] >= need_value
            for need_key, need_value in need.items()
        ])

    def would_afford_better(self, blueprint, robots, materials, robot_index):
        next_round = {
            material: materials[material] + robots[material]['built']
            for material in self.materials
        }
        for robot_type in self.materials[:robot_index]:
            robot = robots[robot_type]
            if self.can_afford(blueprint[robot_type], next_round):
                return True

        return False

    def will_afford_geode_or_obsidian_soon(self, blueprint, robots, materials, limit):
        for in_round in range(1, limit):
            next_round = {
                material: materials[material] + (robots[material]['built'] * in_round)
                for material in self.materials
            }
            if any([
                self.can_afford(blueprint['geode'], next_round),
                self.can_afford(blueprint['obsidian'], next_round),
            ]):
                return True

        return False

    def calculate_blueprint_scores(self, blueprint) -> int:
        cheese = True

        materials = {'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}
        robots = {
            'ore': {'built': 1, 'pending': 0},
            'clay': {'built': 0, 'pending': 0},
            'obsidian': {'built': 0, 'pending': 0},
            'geode': {'built': 0, 'pending': 0},
        }
        max_material_consumption = {
            material: max(robot.get(material, 0) for robot in blueprint.values())
            for material in self.materials
        }
        time_limit = 24

        for minute in range(1, time_limit + 1):
            """
            Order of operations:
            - Purchase new robots
            - Collect ores
            - Activate purchased robots
            """
            print(f'== Minute {minute} ==')

            # Given the current means of production, how far are we from
            # being able to purchase an obsidian or geode robot?
            distance_to_obsidian = 0
            distance_to_geode = 0
            # Does making a purchase of an ore or clay robot increase the distance to obs/geo?
            # If no, then it's a "free" purchase, so do it.

            # Never buy more clay robots than the most expensive robot costs in clay.

            # If we have time to purchase something and have it make a difference
            if minute < time_limit:
                # Can we afford a geode-cracker?
                if self.can_afford(blueprint['geode'], materials):
                    expenditure = ' and '.join([
                        f'{amount} {material}'
                        for material, amount in blueprint['geode'].items()
                    ])
                    print(f'Spend {expenditure} to start building a geode robot.')

                    robots['geode']['pending'] += 1
                    for material, amount in blueprint['geode'].items():
                        materials[material] -= amount

                elif self.can_afford(blueprint['obsidian'], materials):
                    if not self.would_afford_better(blueprint, robots, materials, 1):
                        expenditure = ' and '.join([
                            f'{amount} {material}'
                            for material, amount in blueprint['obsidian'].items()
                        ])
                        print(f'Spend {expenditure} to start building a obsidian robot.')

                        robots['obsidian']['pending'] += 1
                        for material, amount in blueprint['obsidian'].items():
                            materials[material] -= amount

                else:
                    for material in ['clay', 'ore']:
                        # If we're producing more ore per minute than we can consume, don't build more ore robots
                        if material == 'ore' and robots['ore']['built'] > max_material_consumption['ore']:
                            break

                        # If we have more of this material than we're able to consume in the remaining time, don't build
                        if materials[material] > max_material_consumption[material] * (24 - minute):
                            break

                        # Can we afford to build a robot of this type?
                        # Do we _want_ to build one?
                        can_afford = self.can_afford(blueprint[material], materials)

                        limit = min(3, 24 - minute)
                        will_afford_better = self.will_afford_geode_or_obsidian_soon(blueprint, robots, materials,
                                                                                     limit)
                        if can_afford and not will_afford_better:
                            expenditure = ' and '.join([
                                f'{amount} {material}'
                                for material, amount in blueprint[material].items()
                            ])
                            print(f'Spend {expenditure} to start building a {material} robot.')
                            robots[material]['pending'] += 1
                            materials['ore'] -= blueprint[material]['ore']
                            break

            # Run collection
            for material, values in robots.items():
                if count := robots[material]['built']:
                    materials[material] += count
                    print(
                        f"{count} {material} robot(s) collects {count} {material}; you now have {materials[material]} {material}.")

            # Turn pending robots into real ones
            for material, values in robots.items():
                if values['pending'] > 0:
                    robots[material]['built'] += values['pending']
                    robots[material]['pending'] = 0
                    built = robots[material]['built']
                    print(f'The new {material} robot is ready; you now have {built} of them.')

            print()

        return materials['geode']

    def get_max_score(self, blueprint) -> int:
        max_score = 0
        for _ in trange(250_000):
            score = self.calculate_blueprint_scores(blueprint)
            max_score = max(max_score, score)

        return max_score

    def run_step_1(self) -> int:
        # scores = {i: 0 for i in range(len(self.blueprints))}
        scores = map(self.calculate_blueprint_scores, self.blueprints)

        # with Pool(min(os.cpu_count(), len(self.blueprints))) as p:
        #     scores = p.map(self.calculate_blueprint_scores, self.blueprints)

        print(list(scores))
        return sum([
            k + 1 * v
            for k, v in enumerate(scores)
        ])

    def run_step_2(self) -> int:
        ...


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
