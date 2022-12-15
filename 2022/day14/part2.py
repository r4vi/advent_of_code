import itertools
import os
from dataclasses import dataclass
from functools import cached_property
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
    return (start[0] + move[0], start[1] + move[1])


@dataclass(kw_only=True)
class Grid:
    source: tuple[int, int]

    @cached_property
    def max_x(self):
        return max(x for x, y in self.rocks)

    @cached_property
    def min_x(self):
        return min(x for x, y in self.rocks)

    @cached_property
    def max_y(self):
        return max(y for x, y in self.rocks)

    def is_blocked(self, loc: tuple[int, int]) -> bool:
        return loc in self.rocks

    def __post_init__(self):
        self.rocks = set()
        self.sand = set()
        self.min_y = 0

    def is_out_of_bounds(self, loc):
        x, y = loc
        inb = self.min_x <= x < self.max_x and self.min_y <= y <= self.max_y
        return not inb

    def add_line(self, line: list[tuple[int, int]]):
        pairs = itertools.pairwise(line)
        for start, end in pairs:
            if start[0] == end[0]:
                # go down
                direction = 1 if end[1] > start[1] else -1
                for yy in range(start[1], end[1] + direction, direction):
                    self.rocks.add((start[0], yy))
            elif start[1] == end[1]:
                # go right
                direction = 1 if end[0] > start[0] else -1
                for xx in range(start[0], end[0] + direction, direction):
                    self.rocks.add((xx, start[1]))

    def next_coord(self, sand):
        if not self.is_blocked(new := apply_move(sand, DOWN)):
            return new
        elif not self.is_blocked(new := apply_move(sand, LEFT_DOWN)):
            return new
        elif not self.is_blocked(new := apply_move(sand, RIGHT_DOWN)):
            return new
        self.sand.add(sand)
        self.rocks.add(sand)
        return None

    def run(self):
        curr = self.source
        while not (self.source in self.sand):
            curr = self.next_coord(curr)
            if curr:
                if curr[1] >= self.max_y + 2:
                    self.rocks.add(curr)
                    curr = self.source

            else:
                # restart from top
                curr = self.source

        return len(self.sand)


def make_grid(lines: list[list[tuple[int, int]]]):
    all_points = list(itertools.chain.from_iterable(lines))
    all_xs = {x for x, y in all_points}
    all_ys = {y for x, y in all_points}
    min_x, min_y = min(all_xs), min(all_ys)
    max_x, max_y = max(all_xs), max(all_ys)
    grid_height = max_y
    grid_width = max_x - min_x
    grid = Grid(source=SOURCE)
    for line in lines:
        grid.add_line(line)
    return grid


def sample_():
    lines = parse_input(sample)
    grid = make_grid(lines)
    moves = grid.run()

    assert moves == 93, f"moves is {moves}"
    return moves


def main():
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()

    lines = parse_input(input_raw)
    grid = make_grid(lines)
    moves = grid.run()
    return moves


if __name__ == "__main__":
    # print(sample_())
    print(main())
