from collections import Counter
from pprint import pprint
from typing import List, FrozenSet, Tuple

sample_raw = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

sample_part2 = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""


def parse_input(raw_input) -> List[Tuple[List[frozenset], List[frozenset]]]:
    parsed = raw_input.strip().split("\n")
    parsed = [x.split("|") for x in parsed]
    parsed = [
        (
            list(map(frozenset, l.strip().split(" "))),
            list(map(frozenset, r.strip().split(" "))),
        )
        for l, r in parsed
    ]
    return parsed


lookup = [
    frozenset("abcefg"),  # 0
    frozenset("cf"),  # 1, unique, 2
    frozenset("acdeg"),  # 2
    frozenset("acdfg"),  # 3
    frozenset("bcdf"),  # 4, unique, 4
    frozenset("abdfg"),  # 5
    frozenset("abdefg"),  # 6
    frozenset("acf"),  # 7, unique, 3
    frozenset("abcdefg"),  # 8, unique, 7
    frozenset("abcdfg"),  # 9
]

signal_to_length = Counter(len(x) for x in lookup)
uniques_lengths = {k for k, v in signal_to_length.items() if v == 1}


def test_sample_part1():
    parsed = parse_input(sample_raw)
    # don't care about the value of the inputs
    # just the lengths
    parsed_outputs = [x[1] for x in parsed]
    count = 0
    for input in parsed_outputs:
        for s in input:
            if len(s) in uniques_lengths:
                count += 1
    assert count == 26


def test_input_part1():
    with open("./input", "r") as i:
        parsed = parse_input(i.read())

        parsed_outputs = [x[1] for x in parsed]
        count = 0
        for input in parsed_outputs:
            for s in input:
                if len(s) in uniques_lengths:
                    count += 1
        assert count == 390


def solve_pair(pair: Tuple[List[FrozenSet], List[FrozenSet]]):
    inputs, outputs = pair
    possibilities = {}

    # figure out known outputs
    for segment in outputs:
        for real_signal in lookup:
            if len(real_signal) == len(segment):
                possibilities[segment] = real_signal
    # now map knowns to inputs
    knowns = {}
    for i in inputs:
        if i in possibilities:
            knowns[i] = possibilities[i]

    return knowns


def test_part2_sample():
    parsed = parse_input(sample_part2)
    for pair in parsed:
        values = solve_pair(pair)
        assert values == [5, 3, 5, 3]
