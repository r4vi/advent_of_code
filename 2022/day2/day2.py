from pprint import pprint

MOVE_SCORES = {"A": 1, "B": 2, "C": 3}
DRAW_POINTS = 3
WIN_POINTS = 6
LOSE_POINTS = 0


def parse_input(file_name):
    guide = []
    with open(file_name, "r") as input:
        for line in input.readlines():
            if l := line.strip():
                guide.append(tuple(l.split(" ")))
    return guide


def score_round(round_):
    score_table = {
        ("A", "X"): 1 + 3,
        ("A", "Y"): 2 + 6,
        ("A", "Z"): 3 + 0,
        ("B", "X"): 1 + 0,
        ("B", "Y"): 2 + 3,
        ("B", "Z"): 3 + 6,
        ("C", "X"): 1 + 6,
        ("C", "Y"): 2 + 0,
        ("C", "Z"): 3 + 3,
    }
    return score_table[round_]


def score_round_part2(round_):
    score_table = {
        ("A", "X"): 1 + 3,
        ("A", "Y"): 2 + 6,
        ("A", "Z"): 3 + 0,
        ("B", "X"): 1 + 0,
        ("B", "Y"): 2 + 3,
        ("B", "Z"): 3 + 6,
        ("C", "X"): 1 + 6,
        ("C", "Y"): 2 + 0,
        ("C", "Z"): 3 + 3,
    }
    # X desires loss
    # Y desires draw
    # Z desires win
    score_table_desired_outcome = {
        ("A", "X"): "Z",
        ("A", "Y"): "X",
        ("A", "Z"): "Y",
        ("B", "X"): "X",
        ("B", "Y"): "Y",
        ("B", "Z"): "Z",
        ("C", "X"): "Y",
        ("C", "Y"): "Z",
        ("C", "Z"): "X",
    }

    return score_table[(round_[0], score_table_desired_outcome[round_])]


if __name__ == "__main__":

    # part 1
    # sample

    guide = parse_input("./sample")
    pprint(guide)
    scores = [score_round(x) for x in guide]
    pprint(scores)
    assert scores == [8, 1, 6]
    print(sum(scores))

    # part 1
    guide = parse_input("./input")
    scores = [score_round(x) for x in guide]
    pprint(scores)
    print(sum(scores))

    # part 2
    # sample
    guide = parse_input("./sample")
    pprint(guide)
    scores = [score_round_part2(x) for x in guide]
    pprint(scores)
    assert scores == [4, 1, 7]
    print(sum(scores))

    # part 2
    # input
    guide = parse_input("./input")
    pprint(guide)
    scores = [score_round_part2(x) for x in guide]
    pprint(scores)
    print(sum(scores))
