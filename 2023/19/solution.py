from collections import namedtuple


class PartAccepted(Exception):
    pass


class PartRejected(Exception):
    pass


Range = namedtuple('Range', list('xmas'))  # :)


class Day:
    def __init__(self, data: str):
        workflows, parts = data.split('\n\n')
        workflows = self.parse_workflows(workflows)
        self.workflows = self.simplify_workflows(workflows)
        self.parts = self.parse_parts(parts)

    @staticmethod
    def parse_workflows(data):
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

    def simplify_workflows(self, workflows):
        # There are some workflows which always resolve to a specific value
        # This means that referencing workflows can reduce nesting by 1
        simple_workflows = {
            label: rules['else']
            for label, rules in workflows.items()
            if len(set(rules.values())) == 1
        }
        if not simple_workflows:
            return workflows

        for label, result in simple_workflows.items():
            for workflow, rules in workflows.items():
                for calc, dest in rules.items():
                    if dest == label:
                        rules[calc] = result

            workflows.pop(label)

        return self.simplify_workflows(workflows)

    @staticmethod
    def parse_parts(data):
        parts = []
        for part in data.splitlines():
            d = {}
            for params in part[1:-1].split(','):
                k, v = params.split('=')
                d[k] = int(v)
            parts.append(d)
        return parts

    @staticmethod
    def eval_rule(x, m, a, s, rule) -> bool:
        return eval(rule)

    def apply_rule(self, part, workflow_name):
        workflow = self.workflows[workflow_name]
        for rule, destination in workflow.items():
            if rule == 'else' or self.eval_rule(*part.values(), rule):
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

    def run_step_1(self) -> int:
        # 406934
        return sum(self.calculate(part) for part in self.parts)

    def calculate_range(self, r: Range, workflow_name='in') -> int:
        if workflow_name == 'R':
            return 0
        if workflow_name == 'A':
            result = 1
            for low, high in r:
                result *= high - low + 1
            return result

        workflow = self.workflows[workflow_name]
        fallback = workflow.pop('else')

        score = 0
        for rule, destination in workflow.items():
            variable, op, value = rule[0], rule[1], int(rule[2:])
            low, high = getattr(r, variable)
            true_items = (low, value - 1) if op == '<' else (value + 1, high)
            false_items = (value, high) if op == '<' else (low, value)

            if true_items[0] <= true_items[1]:
                score += self.calculate_range(r._replace(**{
                    variable: true_items,
                }), destination)

            if false_items[0] <= false_items[1]:
                r = r._replace(**{
                    variable: false_items,
                })
            else:
                break

        else:
            score += self.calculate_range(r, fallback)

        return score

    def run_step_2(self) -> int:
        ranges = Range(**{k: [1, 4000] for k in 'xmas'})
        # 131192538505367
        return self.calculate_range(ranges)


if __name__ == '__main__':
    from aocd import data
    print(f'Step 1: {Day(data).run_step_1()}')
    print(f'Step 2: {Day(data).run_step_2()}')
