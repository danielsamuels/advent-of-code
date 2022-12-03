import enum
import itertools


class Move(enum.IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3


class Result(enum.IntEnum):
    LOSS = 0
    DRAW = 3
    WIN = 6


move_map: dict[str, Move] = {
    'A': Move.ROCK,
    'B': Move.PAPER,
    'C': Move.SCISSORS,
    'X': Move.ROCK,
    'Y': Move.PAPER,
    'Z': Move.SCISSORS,
}

result_map: dict[str, Result] = {
    'X': Result.LOSS,
    'Y': Result.DRAW,
    'Z': Result.WIN,
}


def calculate_score(opponent: Move, response: Move) -> int:
    result: Result

    if opponent == response:
        result = Result.DRAW
    # Player wins
    elif (
            (response == Move.ROCK and opponent == Move.SCISSORS) or
            (response == Move.SCISSORS and opponent == Move.PAPER) or
            (response == Move.PAPER and opponent == Move.ROCK)
    ):
        result = Result.WIN
    # Opponent wins
    else:
        result = Result.LOSS

    return response + result


def run_part_1(data: str):
    # Play as if XYZ is the response
    games = [game.split(' ') for game in data.split('\n')]
    # Convert moves to enums
    games = [[move_map[opponent], move_map[player]] for opponent, player in games]

    results = itertools.starmap(calculate_score, games)
    score = sum(results)
    print('Score: ', score)


def calculate_response(opponent: str, result: str) -> Move:
    opponent_move = move_map[opponent]
    desired_result = result_map[result]

    if desired_result == Result.DRAW:
        return opponent_move
    elif desired_result == Result.WIN:
        if opponent_move == Move.ROCK:
            return Move.PAPER
        elif opponent_move == Move.PAPER:
            return Move.SCISSORS
        elif opponent_move == Move.SCISSORS:
            return Move.ROCK
    elif desired_result == Result.LOSS:
        if opponent_move == Move.ROCK:
            return Move.SCISSORS
        elif opponent_move == Move.PAPER:
            return Move.ROCK
        elif opponent_move == Move.SCISSORS:
            return Move.PAPER


def run_part_2(data: str):
    # Play as if XYZ is the result
    games = [game.split(' ') for game in data.split('\n')]
    # Convert moves to enums
    games = [[move_map[opponent], calculate_response(opponent, player)] for opponent, player in games]

    results = itertools.starmap(calculate_score, games)
    score = sum(results)
    print('Score: ', score)


if __name__ == '__main__':
    with open('data/day_2.txt', 'r') as f:
        read_data = f.read()

    run_part_2(read_data)
