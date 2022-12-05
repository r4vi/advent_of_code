from functools import reduce
import sys, os
import string
from pathlib import Path
from itertools import zip_longest
import operator

sample = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

PRIORITY = {letter: i + 1 for i, letter in enumerate(string.ascii_letters)}


def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)


def process_input(input_):
    intersections = []
    groups = grouper(input_, 3)
    for group in groups:
        print(f"{group=}")
        group_unique = [set(x) for x in group]
        print(f"{group_unique=}")

        in_common = list(reduce(operator.and_, group_unique))
        intersections.append(PRIORITY[in_common[0]])
        print(f"{in_common=}")

        print(f"sum intersections: {sum(intersections)}")


def main():
    # part 2
    ## sample
    process_input(sample.split())

    ## with input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()
    process_input(input_raw.split())

    return 0


if __name__ == "__main__":
    sys.exit(main())
