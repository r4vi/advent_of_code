import os
from pathlib import Path
from pprint import pprint
import sys
import re
from typing import List

dir_path = Path(os.path.dirname(os.path.realpath(__file__)))


def parse_input(input_):
    state, moves_text = input_.split("\n\n")
    moves = [re.findall(r"\d+", move) for move in moves_text.split("\n")]
    moves = [list(map(int, x)) for x in moves]
    return state.split("\n"), moves


def row_to_blocks(row):
    blocks = []
    lr = len(row)
    chunk_size = lr // 4
    for i in range(0, lr, 4):
        y = row[i : i + 3]
        if y == "   ":
            y = "[_]"
        blocks.append(y)
    return blocks


def build_game(state) -> list[list[str | None]]:
    """
    represent the ship as a list of lists
    e.g.
        [D]
    [N] [C]
    [Z] [M] [P]
     1   2   3
    would return:
    [
     ['Z', 'N'],
     ['M, 'C', 'D'],
     ['P']
    """

    # find the width of the list
    list_width = max(map(int, re.findall(r"\d+", state[-1])))
    list_height = len(state) - 1
    game_state = [[None for x in range(list_height)] for y in range(list_width)]
    for r_index, row in enumerate(state[:-1]):
        row_split = row_to_blocks(row)
        for col_index, container in enumerate(row_split):
            if not container == "[_]":
                game_state[col_index][r_index] = container[1]
    return [list(filter(bool, reversed(x))) for x in game_state]


def apply_move(game_state, n, from_, to):
    from_zero_idx = from_ - 1
    to_zero_idx = to - 1
    to_move = game_state[from_zero_idx][-n:][:]
    game_state[from_zero_idx] = game_state[from_zero_idx][:-n][:]
    game_state[to_zero_idx].extend(to_move)


def apply_moves(game_state, move_list):
    for move in move_list:
        apply_move(game_state, move[0], move[1], move[2])
        pprint(game_state)


def main():
    # part 2
    # input

    input_ = Path("./input").open("r").read()

    state, moves = parse_input(input_)
    game_state: list[list[str]] = build_game(state)
    pprint(game_state)
    apply_moves(game_state, moves)
    pprint(game_state)

    tops = "".join([x[-1] for x in game_state])
    print(f"{tops=}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
