"""
| is a vertical pipe connecting north and south.
- is a horizontal pipe connecting east and west.
L is a 90-degree bend connecting north and east.
J is a 90-degree bend connecting north and west.
7 is a 90-degree bend connecting south and west.
F is a 90-degree bend connecting south and east.
. is ground; there is no pipe in this tile.
S is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the pipe has.
"""
from dataclasses import dataclass, field
from typing import List

NORTH = (0, -1)
SOUTH = (0, 1)
EAST = (1, 0)
WEST = (-1, 0)

JOINTS = {
    "|": [SOUTH, NORTH],
    "-": [EAST, WEST],
    "L": [NORTH, EAST],
    "J": [NORTH, WEST],
    "7": [SOUTH, WEST],
    "F": [SOUTH, EAST],
    "S": [],
    ".": [],
}
CONN_TO_SYM = {frozenset(v): k for k, v in JOINTS.items()}


@dataclass(eq=True, order=True, frozen=True)
class Node:
    pos: tuple[int, int] = field(repr=True)
    sym: str = field(repr=True)

    @property
    def out_pos(self):
        joint_outputs = JOINTS[self.sym]
        return {
            x
            for x in [(self.pos[0] + j[0], self.pos[1] + j[1]) for j in joint_outputs]
            if x[0] > 0 and x[1] > 0
        }


def parse_input(in_):
    with open(in_) as f:
        lines = f.read().strip().splitlines()
    nodes = []
    for y, row in enumerate(lines):
        for x, col in enumerate(row):
            n = Node(sym=col, pos=(x, y))
            # print(n, n.out_pos)
            nodes.append(n)
    return nodes, lines


BOLD = "\033[4m"
END_BOLD = "\033[0m"


def print_map(nodes: List[Node], highlight=None):
    if highlight is None:
        highlight = set()
    all_pos = {n.pos: n for n in nodes}
    max_y = max(n[1] for n in all_pos.keys())
    max_x = max(n[0] for n in all_pos.keys())
    for y in range(max_y):
        for x in range(max_x):
            prefix = ""
            suffix = ""
            if (x, y) in highlight:
                prefix = BOLD
                suffix = END_BOLD

            print(f"{prefix}{all_pos[(x, y)].sym}{suffix}", end="")
        print("")


def determine_start_sym(start, connected_to_start):
    connected_pos = [x.pos for x in connected_to_start]
    reverse_lookup = frozenset(
        [
            (x[0] - start.pos[0], x[1] - start.pos[1]) for x in connected_pos
        ]
    )
    return CONN_TO_SYM[reverse_lookup]

def walk(nodes, start,  seen=None):
    if seen is None:
        seen = set()
    for next_pos in list(start.out_pos):
        if next_pos in seen:
            continue
        next_node = nodes[next_pos]
        seen.add(next_pos)
        walk(nodes, next_node,  seen=seen)
    return seen
def part1(in_):
    nodes, lines = parse_input(in_)
    start = [x for x in nodes if x.sym == "S"][0]
    connected_to_start = [x for x in nodes if start.pos in x.out_pos]
    start_sym = determine_start_sym(start, connected_to_start)
    print(f'Start is {start_sym}')
    # highlight = {x.pos for x in connected_to_start}
    # print(print_map(nodes, highlight=highlight))
    start_determined = Node(sym=start_sym, pos=start.pos)
    nodes_map = {n.pos: n for n in nodes}
    seen = walk(nodes_map, start_determined, seen={start.pos})
    print(f'{len(seen)/2=}')

if __name__ == "__main__":
    import sys
    sys.setrecursionlimit(15000)
    part1("./input.txt")
