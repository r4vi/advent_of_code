import math
from collections import UserDict
from pprint import pprint
from itertools import islice


# import pytest
# from pytest_subtests import subtests


def chunk(l, by):
    chunks = []
    current = []
    for line in l[2:]:
        if not line == by:
            val = []
            if line[0][0].isdigit():
                val = [int(x) for x in line[0].split(" ")]
            else:
                val = line[0]
            current.append(val)
        else:
            chunks.append(current)
            current = []
    chunks.append(current)
    return l[0], *chunks


class MemEfficientMap(UserDict):
    def __init__(self, ranges, name=""):
        super().__init__()
        self.ranges = ranges
        self.name = name

    def __getitem__(self, item):
        for r in self.ranges:
            source_start = r[1]
            source_end = r[1] + r[2]
            dest_start = r[0]
            if source_start <= item < source_end:
                return (item - source_start) + dest_start
        return item

    def backwards(self, item):
        for r in self.ranges:
            source_start = r[1]
            source_end = r[1] + r[2]
            dest_start = r[0]
            dest_end = r[0] + r[2]

            if dest_start <= item < dest_end:
                return (item - dest_start) + source_start
        return item

    def __unicode__(self):
        return f"{self.name or self.ranges}"

    def __str__(self):
        return self.__unicode__()


def make_map(orig):
    return MemEfficientMap(orig[1:], name=orig[0][0])


def parse_input(in_):
    with open(in_, "r") as f:
        lines = [l.strip().split("\n") for l in f.read().strip().splitlines()]
    (
        seeds,
        seed2soil,
        soil2fert,
        fert2water,
        water2light,
        light2temp,
        temp2hum,
        hum2loc,
    ) = list(chunk(lines, [""]))
    seed2soild = make_map(seed2soil)
    soil2fertd = make_map(soil2fert)
    fert2waterd = make_map(fert2water)
    water2lightd = make_map(water2light)
    light2tempd = make_map(light2temp)
    temp2humd = make_map(temp2hum)
    hum2locd = make_map(hum2loc)
    seeds = [int(x) for x in seeds[0].replace("seeds: ", "").split(" ")]
    return seeds, [
        seed2soild,
        soil2fertd,
        fert2waterd,
        water2lightd,
        light2tempd,
        temp2humd,
        hum2locd,
    ]


def part1(in_):
    seeds, lookups = parse_input(in_)
    print(seeds)
    dests = {}
    for seed in seeds:
        print(f"{seed=} ->", end="")
        pos = seed
        for lookup in lookups:
            pos = lookup.get(pos, pos)
            print(f"{pos=} ->", end="")
        dests[seed] = pos
        print("")
    pprint(dests)
    print(min(dests.values()))


def test_mem_map_backwards(subtests):
    ranges = [
        # dest, src, step
        [50, 98, 2],
        [52, 50, 48],
    ]
    m = MemEfficientMap(ranges)
    tests = [(111, 111), (98, 50), (99, 51), (100, 100), (50, 52), (49, 49)]
    for src, dst in tests:
        with subtests.test(msg=f"map from {dst} to {src}"):
            assert m.backwards(dst) == src


def test_mem_map(subtests):
    ranges = [
        # dest, src, step
        [50, 98, 2],
        [52, 50, 48],
    ]
    m = MemEfficientMap(ranges)
    tests = [(111, 111), (98, 50), (99, 51), (100, 100), (50, 52), (49, 49)]
    # for src, dst in tests:
    #     with subtests.test(msg=f"map from {src} to {dst}"):
    #         assert m[src] == dst


def batched(iterable, n):
    "Batch data into tuples of length n. The last batch may be shorter."
    # batched('ABCDEFG', 3) --> ABC DEF G
    if n < 1:
        raise ValueError("n must be at least one")
    it = iter(iterable)
    while batch := tuple(islice(it, n)):
        yield batch


def part2(in_):
    """
    got the answer with brute force approach but
    started to optmise this by trying to walk backards
    but never finished
    """
    seeds, lookups = parse_input(in_)
    print(seeds)
    ranges = [
        (seed_start, seed_start + seed_length)
        for seed_start, seed_length in batched(seeds, 2)
    ]
    print(ranges)
    n = 0
    while True:
        found = False
        for lookup in lookups[::-1]:
            pos = n
            pos = lookup.backwards(pos)
            print(f"{pos=} ->", end="")
        print("")
        for r in ranges:
            if r[0] < n < r[1]:
                print(n, pos)
        n += 1


if __name__ == "__main__":
    # part1("./input.txt")
    part1("./sample.txt")
    # part2("./sample.txt")
    # part2("./sample.txt")
