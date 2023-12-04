from collections import defaultdict


class Day:
    def __init__(self, data: str):
        self.data = data.splitlines()

        self.parsed_rows: dict[int, set] = {}

        for line in self.data:
            game_id, matches = self.parse_row(line)
            self.parsed_rows[game_id] =  matches

    def parse_row(self, line) -> tuple[int, set]:
        game_id, rest = line.split(': ')
        game_id = game_id[5:].strip()

        winners, owned = rest.split(' | ')
        winners = {int(s) for s in winners.split()}
        owned = {int(s) for s in owned.split()}

        matches = winners & owned

        return int(game_id), matches

    def run_step_1(self) -> int:
        # 26,426
        return sum([
            pow(2, len(matches) - 1) if matches else 0
            for matches in self.parsed_rows.values()
        ])

    def run_step_2(self) -> int:
        won_cards = {
            game_id: list(range(game_id + 1, game_id + 1 + len(matches)))
            for game_id, matches in self.parsed_rows.items()
        }

        calculations = {}

        for game_id, cards in reversed(won_cards.items()):
            calculations[game_id] = [game_id]
            for card in cards:
                calculations[game_id].extend(calculations[card])

        # 6,227,972
        return sum(len(v) for v in calculations.values())


if __name__ == "__main__":
    with open(f'input.txt', 'r') as f:
        read_data = f.read()

    day = Day(read_data)

    result = day.run_step_1()
    print(f'Step 1: {result}')

    result_2 = day.run_step_2()
    print(f'Step 2: {result_2}')
