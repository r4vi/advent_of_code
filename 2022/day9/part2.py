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

sample2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20
"""

MOVE_VECS = {"R": (1, 0), "L": (-1, 0), "U": (0, 1), "D": (0, -1)}
MOVE_FMT = {v: k for k, v in MOVE_VECS.items()}


def apply_move(current, move_vec):
    return (
        current[0] + move_vec[0],
        current[1] + move_vec[1],
    )


def is_adj(h, t):
    adj = True
    corr_x = 0
    corr_y = 0
    # too far x left/right:
    diff_x = h[0] - t[0]
    if diff_x > 1:
        adj = False
        corr_x = -1
    elif diff_x < -1:
        adj = False
        corr_x = 1

    # too far y:
    diff_y = h[1] - t[1]
    if diff_y > 1:
        adj = False
        corr_y = -1
    elif diff_y < -1:
        adj = False
        corr_y = 1

    return adj, (corr_x, corr_y)


def main():
    # part 2
    #  sample1
    # all_moves = calculate(sample)
    # print(f"{len(set(all_moves[-1]))}")  # expect 1

    # part 2
    #  sample2
    all_moves = calculate(sample2)
    print(f"{len(set(all_moves[-1]))}")  # expect 36

    # part 1
    ## input
    # dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    # input_raw = (dir_path / Path("./input")).open("r").read()
    # all_moves = calculate(input_raw)
    # print(f"{len(set(all_moves[-1]))}")
    return 0


def calculate(move_txt):
    moves = [
        (MOVE_VECS[d], int(n))
        for (d, n) in [line.split() for line in move_txt.splitlines()]
    ]
    knots = [
        [(0, 0)], # 0, head
        [(0, 0)], # 1
        [(0, 0)], # 2
        [(0, 0)], # 3
        [(0, 0)], # 4
        [(0, 0)], # 5
        [(0, 0)], # 6
        [(0, 0)], # 7
        [(0, 0)], # 8
        [(0, 0)], # 9
    ]

    for move_vec, number_of_moves in moves:
        # pprint(knots)
        for i in range(number_of_moves):
            for idx in range(len(knots)):
                knot = knots[idx]
                if idx == 0:
                    knot.append(apply_move(knot[-1], move_vec))
                    print(f"moving knot[{idx}] {knot[-2]=} to {knot[-1]}")
                else:
                    if idx <= len(knots):
                        curr = knot[-1]
                        prev = knots[idx-1][-1]
                        adj, fix_move = is_adj(curr, prev)
                        if not adj:
                            knot.append(apply_move(curr, fix_move))

    return knots


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
