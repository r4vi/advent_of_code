import itertools
import os
from collections import defaultdict, Counter
from pathlib import Path
from pprint import pprint
import sys

sample = """30373
25512
65332
33549
35390"""


def main():

    # part 1
    ## sample
    pprint(calc_visible_trees(sample))

    # part 1
    ## input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()
    pprint(calc_visible_trees(input_raw))
    return 0


def calc_visible_trees(height_map):
    grid = [list(map(int, list(x.strip()))) for x in height_map.splitlines()]
    size = len(grid[0])
    flat_grid = list(itertools.chain.from_iterable(grid))
    # get_row = lambda row_idx: flat_grid[row_idx * size : (row_idx * size) + size]
    # get_col = lambda col_idx: flat_grid[col_idx : size * size : size]
    get_xy = lambda x, y: flat_grid[(x + (y * size))]
    positions = [(x, y) for x in range(size) for y in range(size)]
    visibility_dict = {}
    for x, y in positions:
        if x == 0 or y == 0 or x == size - 1 or y == size - 1:
            # if tree is on the edge, then it's visible
            visibility_dict[(x, y)] = True
        else:
            me = get_xy(x, y)
            above_pos = [(x, above_ys) for above_ys in range(y - 1, -1, -1)]
            below_pos = [(x, below_ys) for below_ys in range(y + 1, size)]

            left_pos = [(left_xs, y) for left_xs in range(x - 1, -1, -1)]
            right_pos = [(right_xs, y) for right_xs in range(x + 1, size)]

            visible_above = me > max([get_xy(xx, yy) for xx, yy in above_pos])
            visible_below = me > max([get_xy(xx, yy) for xx, yy in below_pos])
            visible_left = me > max([get_xy(xx, yy) for xx, yy in left_pos])
            visible_right = me > max([get_xy(xx, yy) for xx, yy in right_pos])

            visibility_dict[(x, y)] = (
                visible_above or visible_below or visible_right or visible_left
            )
    return Counter(visibility_dict.values())


if __name__ == "__main__":
    sys.exit(main())
