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
    get_xy = lambda x, y: flat_grid[(x + (y * size))]
    positions = [(x, y) for x in range(size) for y in range(size)]

    visibility_dict = {}
    for x, y in positions:
        me = get_xy(x, y)
        above_pos = [(x, above_ys) for above_ys in range(y - 1, -1, -1)]
        below_pos = [(x, below_ys) for below_ys in range(y + 1, size)]

        left_pos = [(left_xs, y) for left_xs in range(x - 1, -1, -1)]
        right_pos = [(right_xs, y) for right_xs in range(x + 1, size)]

        trees_above = [get_xy(xx, yy) for xx, yy in above_pos]
        trees_below = [get_xy(xx, yy) for xx, yy in below_pos]
        trees_left = [get_xy(xx, yy) for xx, yy in left_pos]
        trees_right = [get_xy(xx, yy) for xx, yy in right_pos]

        los_above = calc_los(me, trees_above)
        los_below = calc_los(me, trees_below)
        los_left = calc_los(me, trees_left)
        los_right = calc_los(me, trees_right)

        visibility_dict[(x, y)] = los_right * los_left * los_below * los_above

    return sorted(visibility_dict.values(), reverse=True)[0]


def calc_los(me, trees):
    blocked = False
    los = 0
    for tree in trees:
        if me > tree:
            los += 1
        else:
            blocked = True
            los += 1
            break
    return los


if __name__ == "__main__":
    sys.exit(main())
