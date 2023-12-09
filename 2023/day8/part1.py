from dataclasses import dataclass
from itertools import cycle

import math


@dataclass(eq=True, frozen=True)
class Node:
    left: str
    right: str


def parse_input(in_):
    with open(in_) as f:
        lines = f.read().strip().splitlines()
    nodes_and_children = {}
    directions = lines[0]
    for line in lines[2:]:
        sp_line = line.split(" = ")
        name = sp_line[0]
        children = sp_line[1]
        children = children.strip("()").split(", ")

        nodes_and_children[name] = Node(left=children[0], right=children[1])

    return directions, nodes_and_children


def part1(directions, nodes):
    print(directions)
    print(nodes)
    inf_directions = cycle(directions)
    move_to = "AAA"
    cur = nodes[move_to]
    for idx, move in enumerate(inf_directions, start=1):
        if move == "L":
            move_to = cur.left
        elif move == "R":
            move_to = cur.right
        if move_to == "ZZZ":
            print(f"{idx=}")
            return
        cur = nodes[move_to]


def traverse(nodes, start, directions):
    inf_directions = cycle(directions)
    move_to = start
    cur = nodes[move_to]
    for idx, move in enumerate(inf_directions, start=1):
        print(f'{move_to=}')
        if move == "L":
            move_to = cur.left
        elif move == "R":
            move_to = cur.right
        if move_to.endswith("Z"):
            print(f"{idx=}")
            return idx

        cur = nodes[move_to]


def part2(directions, nodes):
    print(directions)
    print(nodes)
    inf_directions = cycle(directions)
    start_nodes = [p for p in nodes.keys() if p.endswith("A")]
    mvc = []
    for sn in start_nodes:
        mvc.append(traverse(nodes, sn, directions))
    print(math.lcm(*mvc))


if __name__ == "__main__":
    # sample_d, sample_n = parse_input("./input.txt")
    # part1(sample_d, sample_n)
    sample_2d, sample_2n = parse_input("./input.txt")
    part2(sample_2d, sample_2n)
