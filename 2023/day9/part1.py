from itertools import pairwise
from typing import List


def parse_input(in_):
    rows = []
    with open(in_, "r") as f:
        rows = f.read().strip().splitlines()
        rows = [list(map(int, y.split(" "))) for y in rows]
    return rows


def calc_diff2(seq: list):
    diff0 = [b - a for a, b in pairwise(seq)]
    diff_unique = set(diff0)
    return [
        seq[0]
        - (calc_diff2(diff0)[0] if len(diff_unique) > 1 else list(diff_unique)[0])
    ] + seq


def calc_diff(seq: List[int]) -> int:
    diff0 = [b - a for a, b in pairwise(seq)]
    print(f"{seq=}")
    print(f"{diff0=}")
    diff_unique = set(diff0)
    if len(diff_unique) > 1:
        newseq = seq + [seq[-1] + calc_diff(diff0)[-1]]
        print(f"{newseq=}")
    else:
        newseq = seq + [seq[-1] + list(diff_unique)[0]]
    return newseq


def part1(in_):
    nexts = []
    data = parse_input(in_)
    for seq in data:
        nexts.append(calc_diff(seq))
    print(data)
    print(nexts)
    print([x[-1] for x in nexts])
    print(sum([x[-1] for x in nexts]))


def part2(in_):
    nexts = []
    data = parse_input(in_)
    for seq in data:
        nexts.append(calc_diff2(seq))
    print(data)
    print(nexts)
    print([x[0] for x in nexts])
    print(sum([x[0] for x in nexts]))


if __name__ == "__main__":
    # part1("./input.txt")
    part2("./input.txt")
