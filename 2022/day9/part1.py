import itertools
import os
from collections import defaultdict, Counter, deque
from pathlib import Path
from pprint import pprint
import sys

sample = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

MOVE_VECS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
MOVE_FMT = {v: k for k, v in MOVE_VECS.items()}


def apply_move(current, move_vec):
    return (
        current[0] + move_vec[0],
        current[1] + move_vec[1],
    )


def is_adj(h, t):
    return not (abs(h[0] - t[0]) > 1 or abs(h[1] - t[1]) > 1)


def main():
    # part 1
    #  sample
    calculate(sample)

    # part 1
    ## input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    input_raw = (dir_path / Path("./input")).open("r").read()
    calculate(input_raw)
    return 0


def calculate(move_txt):
    moves = [
        (MOVE_VECS[d], int(n))
        for (d, n) in [line.split() for line in move_txt.splitlines()]
    ]
    head = (0, 0)
    tail = (0, 0)
    head_positions = [head]
    tail_positions = {tail}
    print_game_state({head}, 6, 6, {tail})
    for move_vec, number_of_moves in moves:
        print(f"current state: {head=}, {tail=}, moving {move_vec}*{number_of_moves}")
        for i in range(number_of_moves):
            print(f"moving head{head} to")
            head = apply_move(head, move_vec)
            print_game_state({head}, 6, 6, {tail})
            print(f"{head}")

            if not is_adj(head, tail):
                # tail is too far from head so move it closer
                new_tail = head_positions.pop()
                print(f"\tNOT_ADJ - {head=}, {tail=}, {new_tail=}")
                tail = new_tail
                tail_positions.add(tail)
                print_game_state({head}, 6, 6, {tail})
            head_positions.append(head)
    print(f"{tail_positions=}\n{len(tail_positions)=}")
    print_game_state(head_positions, 6, 6, tail_positions)


def print_game_state(head_positions, width, max_y, tail_positions, sep="\n"):
    grid = "=====\n"
    for yy in range(width + 1):
        for xx in range(max_y + 1):
            is_tail_pos = (xx, yy) in tail_positions
            is_head_pos = (xx, yy) in head_positions
            pixel = "."
            if is_tail_pos and is_head_pos:
                pixel = "@"
            elif is_tail_pos:
                pixel = "T"
            elif is_head_pos:
                pixel = "H"
            grid += f"{pixel}"
        grid += "\n"
    print("\n".join(grid.splitlines()[::-1]), sep=sep)


if __name__ == "__main__":
    sys.exit(main())
