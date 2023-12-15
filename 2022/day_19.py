import copy
import math
import operator
import re
from typing import Union

Material = Union['geode', 'obsidian', 'clay', 'ore']
materials: list[Material] = ['geode', 'obsidian', 'clay', 'ore']
time_limit = 24
inf = float('inf')

class Blueprint:
    robot_costs: dict[Material, dict[Material, int]]
    robot_inventory: dict[Material, dict[str, int]]
    material_inventory: dict[Material, int]

    def __init__(self, definition: str):
        results = list(map(int, re.findall(r'(\d+)', definition)))
        self.identifier = results[0]
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
        assert all(v == 0 for v in self.material_inventory.values())

    def calculate_score(self):
        print(f'\n== Blueprint {self.identifier} ==')
        assert all(v == 0 for v in self.material_inventory.values())

        for minute in range(1, time_limit + 1):
            """
            Order of operations:
            - Purchase new robots
            - Collect ores
            - Activate purchased robots
            """
            print(f'\n== Minute {minute} ==')
            self.maybe_make_purchase(minute)
            self.collect_materials()
            self.finish_building_robots()

        return self.material_inventory['geode']

    def purchase_robot(self, robot_type: Material, dry_run=False):
        if not self.can_afford(robot_type):
            raise ValueError('Unable to afford %s robot', robot_type)

        robot_inventory = copy.deepcopy(self.robot_inventory)
        material_inventory = copy.deepcopy(self.material_inventory)

        if not dry_run:
            expenditure = ' and '.join([
                f'{amount} {material}'
                for material, amount in self.robot_costs[robot_type].items()
            ])
            print(f'Spend {expenditure} to start building a {robot_type} robot.')

        robot_inventory[robot_type]['pending'] += 1
        for material, amount in self.robot_costs[robot_type].items():
            material_inventory[material] -= amount

        if not dry_run:
            self.robot_inventory = robot_inventory
            self.material_inventory = material_inventory

        return robot_inventory, material_inventory

    def maybe_make_purchase(self, minute: int):
        # If we're near the end of the cycle, don't attempt to purchase anything
        if minute == time_limit:
            return

        # If we can afford a geode-cracking robot, buy one immediately.
        if self.can_afford('geode'):
            return self.purchase_robot('geode')

        geode_distance = self.distance_to('geode')
        obsidian_distance = self.distance_to('obsidian')
        if self.can_afford('obsidian'):
            #  and geode_distance > 1
            # Will purchasing one of these reduce the geode distance?
            obsidian_ri, obsidian_mi = self.purchase_robot('obsidian', dry_run=True)
            obsidian_gd = self.distance_to('geode', obsidian_ri, obsidian_mi)

            if geode_distance == inf:
                return self.purchase_robot('obsidian')

            if minute + geode_distance > time_limit - 1 and minute + obsidian_gd > time_limit - 1:
                return

            if obsidian_gd <= geode_distance:
                return self.purchase_robot('obsidian')

        # Will we be able to afford a geode or obsidian robot *next* time
        # _and_ have enough time for it to make a difference?

        if minute < time_limit - 1 and geode_distance <= 1 or obsidian_distance <= 1:
            return

        # If purchasing a clay or ore robot reduces the time it takes to get
        # an obsidian or geode robot, then do it. If it makes no difference
        # then do it anyway.
        if self.can_afford('clay'):
            clay_ri, clay_mi = self.purchase_robot('clay', dry_run=True)
            clay_gd = self.distance_to('geode', clay_ri, clay_mi)
            clay_od = self.distance_to('obsidian', clay_ri, clay_mi)
            if clay_gd == inf and clay_od == inf:
                return self.purchase_robot('clay')

            if (clay_gd != inf and clay_gd <= geode_distance) or (clay_od != inf and clay_od <= obsidian_distance):
                return self.purchase_robot('clay')

        # Finally, look at ore robot purchasing.
        if self.can_afford('ore'):
            # If we're already producing more ore than we're able to spend per
            # minute, there's no point in purchasing more ore producing robots.
            if self.robot_inventory['clay']['own'] >= max(robot.get('clay', 0) for robot in self.robot_costs.values()):
                return

            # Now return to the same question that was asked about clay earlier:
            # Does purchasing an ore robot affect the distance to purchasing an obs/geode robot?
            ore_ri, ore_mi = self.purchase_robot('ore', dry_run=True)
            ore_gd = self.distance_to('geode', ore_ri, ore_mi)
            ore_od = self.distance_to('obsidian', ore_ri, ore_mi)
            if ore_gd == inf and ore_od == inf:
                return self.purchase_robot('ore')

            if (ore_gd != inf and ore_gd <= geode_distance) or (ore_od != inf and ore_od <= obsidian_distance):
                return self.purchase_robot('ore')

        # If we have more of this material than we're able to consume in the remaining time, don't build
        # if materials[material] > max_material_consumption[material] * (24 - minute):
        #     break

    def can_afford(self, material: Material, inventory: dict[Material, int] = None) -> bool:
        if inventory is None:
            inventory = self.material_inventory

        return all([
            inventory[material] >= amount
            for material, amount in self.robot_costs[material].items()
        ])

    @property
    def affordable_robots(self) -> list[Material]:
        return [
            material
            for material in materials
            if self.can_afford(material)
        ]

    def distance_to(self,
                    robot_type: Material,
                    robot_inventory: dict[Material, dict[str, int]] = None,
                    material_inventory: dict[Material, int] = None) -> float | int | None:
        costs = self.robot_costs[robot_type]

        if robot_inventory is None:
            robot_inventory = self.robot_inventory

        if material_inventory is None:
            material_inventory = self.material_inventory

        # Do we have at least one of each robot type needed to generate the required resources?
        if not all(robot_inventory[material]['own'] > 0 for material in costs.keys()):
            return inf

        return max([
            math.ceil((costs[material] - material_inventory[material]) / robot_inventory[material]['own'])
            for material in costs.keys()
        ])

    def collect_materials(self):
        for material, values in self.robot_inventory.items():
            if count := values['own']:
                self.material_inventory[material] += count
                print("%(c)s %(m)s robot(s) collects %(c)s %(m)s; you now have %(t)s." % {
                    'c': count,
                    'm': material,
                    't': self.material_inventory[material],
                })

    def finish_building_robots(self):
        for material, values in self.robot_inventory.items():
            if values['pending'] > 0:
                self.robot_inventory[material]['own'] += values['pending']
                self.robot_inventory[material]['pending'] = 0
                own = self.robot_inventory[material]['own']
                print(f'The new {material} robot is ready; you now have {own} of them.')

        # We should have no more pending robots
        assert not [r for r, v in self.robot_inventory.items() if v['pending'] > 0]


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

    def run_step_1(self) -> int:
        scores = list(map(operator.methodcaller('calculate_score'), self.blueprints))

        # with Pool(min(os.cpu_count(), len(self.blueprints))) as p:
        #     scores = p.map(self.calculate_blueprint_scores, self.blueprints)

        # Should be [9, 12]
        print(scores)
        return sum([
            (k + 1) * v
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
