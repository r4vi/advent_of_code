import itertools
import os
from enum import Enum
from pathlib import Path
from pprint import pprint
import sys
from types import NoneType
import functools
from input_data import small, big, small2
from itertools import pairwise, islice, zip_longest


# from itertools recipes
def batched(iterable, n):
    "Batch data into lists of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError('n must be at least one')
    it = iter(iterable)
    while (batch := list(islice(it, n))):
        yield batch


TAB = '\t'

class Comparison(Enum):
    LEFT_WINS = -1
    EQ = 0
    RIGHT_WINS = 1

def cmp(l, r, num_rec=0) -> Comparison:
    t_l, t_r = type(l), type(r)
    tabs = TAB * num_rec
    print(f"{tabs}- Compare {l} vs {r}")
    if t_l == t_r == int:
        if l < r:
            print(f"{tabs}- Left side is smaller, so inputs are in the right order")
            return Comparison.LEFT_WINS
        elif l == r:
            return Comparison.EQ
        elif l > r:
            return Comparison.RIGHT_WINS
    elif t_l == int and t_r == list:
        return cmp([l], r, num_rec=num_rec+1)
    elif t_l == list and t_r == int:
        return cmp(l, [r], num_rec=num_rec+1)
    elif t_l == t_r == list:
        il = iter(l)
        ir = iter(r)
        l_complete = r_complete = False
        while True:
            try:
                next_l = next(il)
            except StopIteration:
                l_complete = True
            try:
                next_r = next(ir)
            except StopIteration:
                r_complete = True

            if l_complete and r_complete:
                return Comparison.EQ
            if l_complete and not r_complete:
                return Comparison.LEFT_WINS
            if r_complete and not l_complete:
                return Comparison.RIGHT_WINS

            n_cmp = cmp(next_l, next_r, num_rec=num_rec+1)
            if n_cmp != Comparison.EQ:
                return n_cmp


def cmp2(a,b) -> int:
    return cmp(a,b).value

def main():
    # part 1
    ## sample
    # right_order_indexes = []
    # pairs = batched(big, 2)
    # for idx, pair in enumerate(pairs):
    #     left, right = pair
    #     print(f"== Pair {idx + 1}")
    #     outcome = cmp(left, right)
    #     if outcome == Comparison.LEFT_WINS:
    #         right_order_indexes.append(idx + 1)
    #
    # print(f"{right_order_indexes=}, sum: {sum(right_order_indexes)}")

    # part 2
    ## sample
    decoder = [[[2]], [[6]]]

    i = small + decoder
    s = sorted(i, key=functools.cmp_to_key(cmp2))
    pprint(s)
    assert s == small2

    i = big + decoder
    s = sorted(i, key=functools.cmp_to_key(cmp2))
    s1, s2 = s.index(decoder[0])+1, s.index(decoder[1])+1
    pprint(f"{s1=} * {s2=} ==> {s1*s2}")

    return 0


if __name__ == "__main__":
    main()
