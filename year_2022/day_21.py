from collections import defaultdict

import sympy


class Day:
    monkeys = defaultdict(dict)

    def __init__(self, data: str):
        for row in data.splitlines():
            monkey, value = row.split(': ')
            try:
                self.monkeys[monkey]['value'] = int(value)
            except ValueError:
                self.monkeys[monkey]['formula'] = value.split(' ')

    def run_step_1(self) -> int:
        # Perform replacement of any formula segments we can
        while self.monkeys['root'].get('value') is None:
            monkeys = self.monkeys.copy()
            for monkey, data in monkeys.items():
                if formula := data.get('formula'):
                    t1, operation, t2 = formula
                    self.monkeys[monkey]['formula'][0] = self.monkeys[t1].get('value', t1)
                    self.monkeys[monkey]['formula'][2] = self.monkeys[t2].get('value', t2)

                    # Do we have two numbers yet?
                    try:
                        n1, n2 = int(self.monkeys[monkey]['formula'][0]), int(self.monkeys[monkey]['formula'][2])
                        # We do! Perform the operation and set the value.
                        if operation == '+':
                            self.monkeys[monkey]['value'] = n1 + n2
                        elif operation == '-':
                            self.monkeys[monkey]['value'] = n1 - n2
                        elif operation == '*':
                            self.monkeys[monkey]['value'] = n1 * n2
                        elif operation == '/':
                            self.monkeys[monkey]['value'] = n1 / n2

                        self.monkeys[monkey]['formula'] = None

                    except ValueError:
                        # Not yet!
                        pass

        return self.monkeys['root']['value']

    def run_step_2(self) -> int:
        self.monkeys['root']['formula'][1] = '='
        del self.monkeys['humn']['value']
        self.monkeys['humn']['formula'] = ['humn', '+', 'humn']

        # Determine which monkeys are ultimately dependent on humn
        dependent_monkeys = set()
        monkey_added = True
        while monkey_added:
            monkey_added = False

            for monkey, data in self.monkeys.items():
                if monkey in dependent_monkeys:
                    continue

                if formula := data.get('formula'):
                    t1, _, t2 = formula
                    if 'humn' in [t1, t2] or t1 in dependent_monkeys or t2 in dependent_monkeys:
                        dependent_monkeys.add(monkey)
                        monkey_added = True

        print()
        print(f'Dependent monkeys are: {dependent_monkeys}')

        while self.monkeys['root'].get('value') is None:
            monkeys = self.monkeys.copy()
            for monkey, data in monkeys.items():
                if formula := data.get('formula'):
                    t1, operation, t2 = formula
                    self.monkeys[monkey]['formula'][0] = self.monkeys[t1].get('value', t1)
                    self.monkeys[monkey]['formula'][2] = self.monkeys[t2].get('value', t2)

                    # Do we have two numbers yet?
                    try:
                        n1, n2 = int(self.monkeys[monkey]['formula'][0]), int(self.monkeys[monkey]['formula'][2])
                        # We do! Perform the operation and set the value.
                        value = eval(f'{n1} {operation} {n2}')
                        # print(f'Calculated value for {monkey}: {value}')
                        self.monkeys[monkey]['value'] = value
                        self.monkeys[monkey]['formula'] = None

                    except ValueError:
                        # Not yet!
                        pass

            # Are the only monkeys left with formulas the dependent monkeys?
            remaining_monkeys = set([
                monkey
                for monkey, data in self.monkeys.items()
                if data.get('formula')
            ])
            if remaining_monkeys <= dependent_monkeys:
                print('== Only dependent monkeys remain ==')
                other_monkeys = set(dependent_monkeys) - {'root', 'humn'}

                # Time to do some calculating!
                target_1, _, target_2 = self.monkeys['root']['formula']
                print(self.monkeys['root']['formula'])
                # Build up the full formula for each target
                formulas = []
                for target in [target_1, target_2]:
                    print(f'=> {target}')
                    # Check to see if the target actually has a value first
                    if (value := self.monkeys[target].get('value')) is not None:
                        formulas.append(value)
                    else:
                        formula = ' '.join(str(v) for v in self.monkeys[target]['formula'])
                        while any(m in formula for m in other_monkeys):
                            for m in other_monkeys:
                                if m in formula:
                                    formula = formula.replace(m, '(' + ' '.join(str(v) for v in self.monkeys[m]['formula']) + ')')

                        formulas.append(formula)

                if isinstance(formulas[0], int):
                    to_eval = f'({formulas[1]}) - {formulas[0]}'
                elif isinstance(formulas[1], int):
                    to_eval = f'({formulas[0]}) - {formulas[1]}'
                else:
                    raise Exception('Both sides are equations!')

                humn = sympy.symbols('humn')
                equation = sympy.parse_expr(to_eval)
                eq_res = sympy.solve(equation)
                return eq_res[0]
                print()


        return 44


if __name__ == "__main__":
    test_filename = __file__.split('\\')[-1].split('.py')[0]
    with open(f'data/{test_filename}.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    # result = day.run_step_1()
    # print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
