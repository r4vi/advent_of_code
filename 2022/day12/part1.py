import enum
import os
import random
import sys
from collections import defaultdict
from itertools import repeat
from operator import itemgetter
from pathlib import Path
from pprint import pprint

import pytest

sample = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""


class Directions(enum.Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, 1)
    DOWN = (0, -1)


BOLD = "\033[1m"
UNDERLINE = "\033[4m"
END_YELLOW = END_BOLD = END_UNDERLINE = "\033[0m"
YELLOW = "\33[33m"


def apply_move(current, move_vec):
    return (
        current[0] + move_vec[0],
        current[1] + move_vec[1],
    )


def get_possible_moves(seen: list[tuple[int, int]], current, width, height):
    moves = [apply_move(current, d.value) for d in Directions]
    return [
        m
        for m in moves
        if (m not in seen)
        and (m[0] >= 0 and m[1] >= 0)
        and (m[0] < width and m[1] < height)
    ]


@pytest.mark.parametrize(
    "seen, current, width, height, expected",
    [
        ([(0, 0)], (0, 0), 5, 5, [(0, 1), (1, 0)]),
        ([(0, 0), (0, 1)], (0, 1), 5, 5, [(1, 1), (0, 2)]),
        ([(0, 0), (0, 1), (1, 1)], (1, 1), 5, 5, [(1, 0), (1, 2), (2, 1)]),
    ],
)
def test_get_possible_moves(seen, current, width, height, expected):
    result = get_possible_moves(seen, current, width, height)
    assert set(result) == set(expected)


def letter_to_int(s):
    # will turn a-z to 0-25
    # will turn S into -14
    # and E into -28
    if ord(s) - 97 == -28:
        return 26
    if ord(s) - 97 == -14:
        return -1
    return ord(s) - 97


def print_grid(grid, seen, current):
    for y, row in enumerate(grid):
        print(f"{UNDERLINE}{y:3}{END_UNDERLINE}", end="\t")
        for x, col in enumerate(row):
            prefix = suffix = ""
            if (x, y) in seen:
                prefix = YELLOW
                suffix = END_YELLOW
            if (x, y) == current:
                prefix = BOLD
                suffix = END_BOLD
            print(f"{prefix}{col:3}{suffix}", end="\t")
        print()


def main():
    # part 1
    # sample
    print(calculate(sample))

    # part 1
    ## input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    input_raw = (dir_path / Path("./input")).open("r").read()
    print(calculate(input_raw))

    return 0


def calculate(in_):
    lines = in_.splitlines()
    width = len(lines[0])
    height = len(lines)
    grid = [list(map(letter_to_int, x)) for x in [list(y) for y in lines]]
    # current = top left
    adj_map = {}

    # precompute all possible moves
    start = None
    end = None
    for y in range(height):
        for x in range(width):
            current_val = get_xy(grid, x, y)
            if current_val == -1:
                start = (x, y)
            if current_val == 26:
                end = (x, y)
            current_val_pos = max(current_val, 0)
            moves = get_possible_moves([], (x, y), width, height)
            valid_moves = []
            for possible in moves:
                move_val = get_xy(grid, possible[0], possible[1])
                if move_val <= current_val_pos + 1:
                    valid_moves.append(possible)

            adj_map[(x, y)] = valid_moves

    visited = set()
    unvisited = set(adj_map.keys())
    node_distance = defaultdict(lambda: sys.maxsize)
    node_distance[start] = 0

    while end not in visited:
        current = min(unvisited, key=node_distance.__getitem__)
        for node in adj_map[current]:
            if node not in visited:
                if node_distance[current] + 1 < node_distance[node]:
                    node_distance[node] = node_distance[current] + 1
        visited.add(current)
        unvisited.remove(current)

    return node_distance[end]


def get_xy(grid, x, y):
    return grid[y][x]


if __name__ == "__main__":
    sys.exit(main())
