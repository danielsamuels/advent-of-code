RED_LIMIT = 12
GREEN_LIMIT = 13
BLUE_LIMIT = 14

limits = {
    'red': 12,
    'green': 13,
    'blue': 14,
}


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

    def run_step_1(self) -> int:
        valid_ids = []
        for line in self.data:
            ok = True

            parts = line.split(': ')
            game_id = parts[0][5:]
            pulls = parts[1].split('; ')
            for pull in pulls:
                # ['3 blue', '4 red']
                num_colours = pull.split(', ')
                for colour in num_colours:
                    num, colour = colour.split(' ')
                    if int(num) > limits[colour]:
                        ok = False
                        break

            if ok:
                valid_ids.append(game_id)

        return sum(int(id_) for id_ in valid_ids)


    def run_step_2(self) -> int:
        results = []
        for line in self.data:
            fewest = {
                'red': None,
                'green': None,
                'blue': None,
            }
            parts = line.split(': ')
            game_id = parts[0][5:]
            pulls = parts[1].split('; ')
            for pull in pulls:
                # ['3 blue', '4 red']
                num_colours = pull.split(', ')
                for colour in num_colours:
                    num, colour = colour.split(' ')
                    num = int(num)
                    if fewest[colour] is None:
                        fewest[colour] = num
                    elif num > fewest[colour]:
                        fewest[colour] = num

            results.append(fewest)

        return sum(r['red'] * r['green'] * r['blue'] for r in results)

if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
