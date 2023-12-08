from collections import Counter
from functools import total_ordering, cached_property

ORDER = {v: k for k, v in enumerate(reversed("AKQJT98765432"))}


@total_ordering
class Hand:
    # sorted_cards: str
    cards: str

    def __init__(self, cards: str):
        self.cards = cards

    @cached_property
    def sorted_cards(self):
        return "".join(sorted(self.cards, key=lambda x: ORDER[x], reverse=True))

    @cached_property
    def counts(self):
        return Counter(self.cards)

    @cached_property
    def n_of_a_kind(self):
        return self.counts.most_common(1)[0][1]

    @cached_property
    def full_house(self):
        return {x[1] for x in self.counts.most_common(2)} == {2, 3}

    @cached_property
    def rank_of_hand(self):
        m = tuple(x[1] for x in self.counts.most_common())
        match m:
            case (5, *rest):
                return 6
            case (4, 1):
                return 5
            case (3, 2):
                return 4

            # 3 of a kind
            case (3, 1, 1):
                return 3

            # 2 pair
            case (2, 2, 1):
                return 2

            # 1 pair
            case (2, *rest):
                return 1
        # high card
        return 0

    def __eq__(self, other):
        return self.sorted_cards == other.sorted_cards

    def __lt__(self, other: "Hand"):
        # # 5 kind
        # # 4 kind
        # # 3+2 kind
        # # 2+2 kind
        # # 2 kind
        # # high card

        a = self.rank_of_hand
        b = other.rank_of_hand
        if a != b:
            return a < b
        else:
            for c in zip(self.sorted_cards, other.sorted_cards):
                if c[0] == c[1]:
                    continue
                if ORDER[c[0]] < ORDER[c[1]]:
                    return True
                if ORDER[c[1]] < ORDER[c[0]]:
                    break
        return False

    def __repr__(self):
        return f"Hand({self.cards})"


def parse_input(in_):
    with open(in_, "r") as f:
        lines = [
            (Hand(a), int(b))
            for a, b in [x.split(" ") for x in f.read().strip().splitlines()]
        ]
        return lines


def score(h):
    return h[0]


def part1(in_):
    hands = parse_input(in_)
    print(f"{hands=}")
    ordered_hands = sorted(hands, key=score)
    print(f"{ordered_hands=}")
    ranked_hands = [(h[0], h[1] * (idx + 1)) for (idx, h) in enumerate(ordered_hands)]
    print(f"{ranked_hands=}")
    print(sum(x[1] for x in ranked_hands))


if __name__ == "__main__":
    print(ORDER)
    part1("./sample.txt")
    part1("./input.txt")
    # sample order = 32T3K, KTJJT, KK677, T55J5, QQQJA
