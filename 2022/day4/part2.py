import os
from pathlib import Path
from pprint import pprint
import sys

sample = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""


def parse_input(input_):
    ranges = []
    for line in input_.split():
        elf1, elf2 = line.split(",")
        elf1 = tuple([int(x) for x in elf1.split("-")])
        elf2 = tuple([int(x) for x in elf2.split("-")])
        ranges.append((elf1, elf2))
    return ranges


def overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    for x in range(b[0], b[1] + 1):
        if a[0] <= x <= a[1]:
            return True
        return False


def main():

    # part 1
    ## sample
    parsed = parse_input(sample)
    pprint(parsed)
    full_overlaps = 0
    for elf_pair in parsed:
        elf1, elf2 = elf_pair
        if overlaps(elf1, elf2) or overlaps(elf2, elf1):
            full_overlaps += 1
    print(f"{full_overlaps=}")

    # part 1
    ## input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()
    parsed = parse_input(input_raw)
    pprint(parsed)
    full_overlaps = 0
    for elf_pair in parsed:
        elf1, elf2 = elf_pair
        if overlaps(elf1, elf2) or overlaps(elf2, elf1):
            full_overlaps += 1
    print(f"{full_overlaps=}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
