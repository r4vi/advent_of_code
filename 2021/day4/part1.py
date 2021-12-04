import itertools
from typing import Set, List

import pytest

sample_raw = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""


def parse_input(raw: str):
    lines = raw.split("\n")
    bingo_numbers = [int(x) for x in lines[0].split(",")]
    bingo_cards = []
    current_card = []
    for line in lines[2:]:
        if line == "":
            bingo_cards.append(current_card[:])
            current_card = []
        else:
            current_card.append([int(x) for x in line.split()])
    bingo_cards.append(current_card)
    return bingo_numbers, bingo_cards


@pytest.fixture
def parsed_sample():
    return parse_input(sample_raw)


def cols(card):
    return [list(i) for i in zip(*card)]


# def col(card, n):
#     # transpose list of lists
#     transposed = cols(card)
#     return row(transposed, n)


def flattened(card) -> Set[int]:
    return set(itertools.chain.from_iterable(card))


def check_card(card, drawn):
    # does a card win?

    # yes if any row or any column is a subset of the drawn numbers so far
    return any(
        [True for x in card if set(x).issubset(drawn)]
        + [True for x in cols(card) if set(x).issubset(drawn)]
    )


def score(card, drawn, last):
    unmatched = flattened(card) - drawn
    score_ = sum(unmatched) * last
    print(f"\tScoring a winner: {score_}")
    return score_


def bingo(bingo_ns: List[int], cards):
    # can't win with less than 5 draws so only check after that
    drawn = set(bingo_ns[:4])
    for draw in bingo_ns[4:]:
        drawn.add(draw)

        for card in cards:
            if check_card(card, drawn):
                return score(card, drawn, draw)


def bingo_last(bingo_ns: List[int], cards):
    # can't win with less than 5 draws so only check after that
    drawn = []
    winning_scores = []
    losers = cards
    winners = []
    for draw in bingo_ns:
        print(f"Numbers left to draw: {len(bingo_ns) - len(drawn)}")
        drawn.append(draw)
        print(
            f"Cards left without winning: {len(cards)}, winners: {len(winning_scores)}"
        )

        for loser in losers:
            if check_card(loser, drawn):
                winners.append(loser)
                winning_scores.append(score(loser, set(drawn), draw))

                # card has already won so remove it from the list for the next draw
                losers.remove(loser)

    return winning_scores[-1]


def test_part_one_with_sample(parsed_sample):
    assert bingo(*parsed_sample) == 4512


def read_input(input_file="./input"):
    with open(input_file, "r") as input:
        return input.read().strip()


def test_part_one_with_input():
    raw = read_input()
    numbers, cards = parse_input(raw)
    winner_score = bingo(numbers, cards)
    print(winner_score)


def test_part_two_with_sample(parsed_sample):
    win_score = bingo_last(*parsed_sample)
    assert win_score == 1924


def test_part_two_with_input():
    raw = read_input()
    numbers, cards = parse_input(raw)
    winner_score = bingo_last(numbers, cards)
    print(winner_score)
    assert winner_score == 23541
