from collections import defaultdict, Counter
from itertools import chain

sample_raw = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def parse_input(raw):
    coord_pairs = [x.split(" -> ") for x in raw.strip().split("\n")]
    coord_pairs = [
        (tuple(map(int, z[0].split(","))), tuple(map(int, z[1].split(","))))
        for z in coord_pairs
    ]
    return coord_pairs


def filter_horiz_and_vertical(lines):
    return [x for x in lines if x[0][0] == x[1][0] or x[0][1] == x[1][1]]


def expand_x(from_x, to_x, y):
    expanded_x = []
    if from_x > to_x:
        to_x, from_x = from_x, to_x
    for i in range(from_x, to_x + 1):
        expanded_x.append((i, y))
    return expanded_x


def expand_y(from_y, to_y, x):
    expanded_y = []
    if from_y > to_y:
        to_y, from_y = from_y, to_y
    for i in range(from_y, to_y + 1):
        expanded_y.append((x, i))
    return expanded_y


def expand_diagonal(from_x, from_y, to_x, to_y):
    direction_x = 1 if from_x < to_x else -1
    direction_y = 1 if from_y < to_y else -1
    return list(
        zip(
            range(from_x, to_x + direction_x, direction_x),
            range(from_y, to_y + direction_y, direction_y),
        )
    )


def expand(lines):
    expanded = []
    for from_to in lines:
        from_x = from_to[0][0]
        from_y = from_to[0][1]

        to_x = from_to[1][0]
        to_y = from_to[1][1]

        if from_x != to_x and from_y != to_y:
            expanded.extend(expand_diagonal(from_x, from_y, to_x, to_y))
        elif from_x == to_x:
            expanded.extend(expand_y(from_y, to_y, from_x))
        elif from_y == to_y:
            expanded.extend(expand_x(from_x, to_x, from_y))
    return expanded


def test_expand_lines():
    t1 = [((0, 9), (5, 9))]
    assert expand(t1) == [(0, 9), (1, 9), (2, 9), (3, 9), (4, 9), (5, 9)]

    assert expand([((1, 1), (1, 3))]) == [(1, 1), (1, 2), (1, 3)]

    assert expand([((9, 7), (7, 7))]) == [(7, 7), (8, 7), (9, 7)]


def test_expand_diagonal():
    assert expand([(1, 1), (3, 3)]) == [(1, 1), (2, 2), (3, 3)]
    assert expand([(9, 7), (7, 9)]) == [(7, 9), (8, 8), (9, 7)]


def show(lines):
    flat_pairs = expand(lines)
    return sum(1 for k, v in Counter(flat_pairs).items() if v >= 2)


def test_sample_part1():
    pairs = parse_input(sample_raw)
    lines = filter_horiz_and_vertical(pairs)
    matches = show(lines)
    assert matches == 5


def test_input_part1():
    with open("./input", "r") as i:
        pairs = parse_input(i.read())
        lines = filter_horiz_and_vertical(pairs)
        matches = show(lines)
        print(matches)


def test_sample_part2():
    pairs = parse_input(sample_raw)
    matches = show(pairs)
    assert matches == 12


def test_input_part2():
    with open("./input", "r") as i:
        pairs = parse_input(i.read())
        matches = show(pairs)
        print(matches)
