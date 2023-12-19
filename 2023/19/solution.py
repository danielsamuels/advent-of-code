import itertools

from tqdm import tqdm


class PartAccepted(Exception):
    pass


class PartRejected(Exception):
    pass


class Day:
    def __init__(self, data: str):
        workflows, parts = data.split('\n\n')
        self.workflows = self.parse_workflows(workflows)
        self.parts = self.parse_parts(parts)

    def parse_workflows(self, data):
        workflows = {}
        for workflow in data.splitlines():
            name, rest = workflow[:-1].split('{')
            rules = rest.split(',')
            conditions = {}
            for rule in rules:
                if ':' not in rule:
                    conditions['else'] = rule
                    continue

                condition, target = rule.split(':')
                conditions[condition] = target

            workflows[name] = conditions

        return workflows

    def parse_parts(self, data):
        parts = []
        for part in data.splitlines():
            d = {}
            for params in part[1:-1].split(','):
                k, v = params.split('=')
                d[k] = int(v)
            parts.append(d)
        return parts

    def eval_rule(self, x, m, a, s, rule) -> bool:
        return eval(rule)

    def apply_rule(self, part, workflow_name):
        workflow = self.workflows[workflow_name]
        for rule, destination in workflow.items():
            if rule == 'else':
                if destination == 'A':
                    raise PartAccepted
                if destination == 'R':
                    raise PartRejected

                return self.apply_rule(part, destination)

            result = self.eval_rule(part['x'], part['m'], part['a'], part['s'], rule)
            if result:
                if destination == 'A':
                    raise PartAccepted
                if destination == 'R':
                    raise PartRejected

                return self.apply_rule(part, destination)

    def calculate(self, part) -> int:
        try:
            self.apply_rule(part, 'in')
        except PartAccepted:
            return sum(part.values())
        except PartRejected:
            return 0

        raise Exception('wat?')

    def run_step_1(self) -> int:
        return sum(self.calculate(part) for part in self.parts)

    def run_step_2(self) -> int:
        # 131192538505367
        xr = mr = ar = sr = range(1, 4001)
        p = itertools.product(xr, mr, ar, sr)
        return sum(
            self.calculate({'x': x, 'm': m, 'a': a, 's': s})
            for x, m, a, s in tqdm(p, total=4000 * 4000 * 4000 * 4000)
        )


if __name__ == '__main__':
    from aocd import data
    # print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
