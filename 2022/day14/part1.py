import itertools
import os
from dataclasses import dataclass
from pathlib import Path

# Cooridnate system = (units_right, units down)
# units down start from 0 and go up, e.g. 1 level down is (0, 1)
# units right are a number around 500, eg 1 unit right is (501, 0)

SOURCE = (500, 0)
TAB = "\t"

# move vecs
LEFT_DOWN = (-1, 1)
RIGHT_DOWN = (1, 1)
DOWN = (0, 1)

sample = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


def parse_input(s: str):
    ret = []
    for ln in s.splitlines():
        line_coords = []
        coords_str = [x.strip() for x in ln.split("->")]
        for coord_str in coords_str:
            x_, y_ = coord_str.split(",")
            x = int(x_)
            y = int(y_)
            line_coords.append((x, y))
        ret.append(line_coords)
    return ret

def apply_move(start, move):
    return (
        start[0] + move[0],
        start[1] + move[1]
    )

@dataclass(kw_only=True)
class Grid:
    height: int
    width: int
    source: tuple[int, int]
    orig_x_offset: int = 0

    @property
    def source_native(self):
        return self.source[0] - self.orig_x_offset, self.source[1]

    def __post_init__(self):
        self.data = [['.' for x in range(self.width+1)] for y in range(self.height+1)]

        self.set_xy(self.source_native[0], self.source_native[1], "+")

    def get_xy(self, x, y):
        return self.data[y][x]

    def set_xy(self, x, y, v: str):
        print(f"\tsetting {x},{y} to {v}")
        self.data[y][x] = v

    def get_xy_orig(self, x, y):
        return self.get_xy(x - self.orig_x_offset, y)

    def set_xy_orig(self, x, y, v):
        self.set_xy(x - self.orig_x_offset, y, v)

    def is_in_bounds(self, loc):
        x, y = loc
        return 0 <= x < self.width and 0 <= y <= self.height

    def get_until_blocked(self, x, y) -> list[tuple[int, int]]:
        ret = []
        for y_dest in range(y, self.height):
            dest_val = self.get_xy(x, y_dest)
            if dest_val in ('.', '+'):
                ret.append((x, y_dest))
            else:
                break
        return ret

    def add_line(self, line: list[tuple[int, int]]):
        pairs = itertools.pairwise(line)
        for start, end in pairs:
            # print(f'line between {start}->{end}')
            # print(f"{self}")
            if start[0] == end[0]:
                # go down
                direction = 1 if end[1] > start[1] else -1
                for yy in range(start[1], end[1] + direction, direction):
                    self.set_xy_orig(start[0], yy, "#")
            elif start[1] == end[1]:
                # go right
                direction = 1 if end[0] > start[0] else -1
                for xx in range(start[0], end[0] + direction, direction):
                    self.set_xy_orig(xx, start[1], "#")

    def try_settle(self, loc):


        dd = apply_move(loc, DOWN)
        if self.is_in_bounds(dd):
            down_clear = self.get_xy(*dd) == '.'
            if down_clear:
                return self.try_settle(dd)
        else:
            print(f'oob {dd=}')

        dl = apply_move(loc, LEFT_DOWN)
        if self.is_in_bounds(dl):
            left_clear = self.get_xy(*dl) == '.'
            if left_clear:
                return self.try_settle(dl)
        else:
            print(f'oob {dl=}')

        dr = apply_move(loc, RIGHT_DOWN)
        if self.is_in_bounds(dr):
            right_clear = self.get_xy(*dr) == '.'
            if right_clear:
                return self.try_settle(dr)
        else:
            print(f'oob {dr=}')
        # can't go anywhere so settle here

        if self.is_in_bounds(loc):
            if self.source_native != loc:
                self.set_xy(loc[0], loc[1], 'o')
                return True
        else:
            print(f'oob {loc=}')
            return False

        return False



    def tick(self) -> bool:
        return self.try_settle(self.source_native)

    def __str__(self):
        ret = ""
        for i, y in enumerate(self.data):
            ret += f"{i:4}{TAB}"
            for col in y:
                ret += f"{col:2}"
            ret += "\n"
        return ret


def make_grid(lines: list[list[tuple[int, int]]]):
    all_points = list(itertools.chain.from_iterable(lines))
    all_xs = {x for x, y in all_points}
    all_ys = {y for x, y in all_points}
    min_x, min_y = min(all_xs), min(all_ys)
    max_x, max_y = max(all_xs), max(all_ys)
    grid_height = max_y
    grid_width = max_x - min_x
    grid = Grid(
        height=grid_height, width=grid_width, orig_x_offset=min_x, source=SOURCE
    )
    for line in lines:
        grid.add_line(line)
    return grid


def sample_():
    lines = parse_input(sample)
    grid = make_grid(lines)
    print(str(grid))
    moves = 0
    while grid.tick():
        moves += 1

    assert moves == 24, f"moves is {moves}"
    return moves

def main():

    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()

    lines = parse_input(input_raw)
    grid = make_grid(lines)
    print(str(grid))
    moves = 0
    while grid.tick():
        moves += 1

    return moves

if __name__ == "__main__":
    # print(sample_())
    print(main())
