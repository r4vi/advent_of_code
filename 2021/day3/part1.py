import operator

import pytest
from collections import Counter


@pytest.fixture
def sample():
    return [
        "00100",
        "11110",
        "10110",
        "10111",
        "10101",
        "01111",
        "00111",
        "11100",
        "10000",
        "11001",
        "00010",
        "01010",
    ]


def read_input(input_file="./input"):
    with open(input_file, "r") as input:
        return [x.strip() for x in input.readlines()]


def test_example(sample):
    counters = calculate_counts(sample)

    # gamma
    # first column
    val, count = counters[0].most_common()[0]
    assert val == "1"
    assert count == 7

    # second column
    val, count = counters[1].most_common()[0]
    assert val == "0"
    assert count == 7

    gamma = calculate_gamma(counters)
    assert gamma == "10110"

    epsilon = calculate_epsilon(counters)
    assert epsilon == "01001"

    assert 198 == int(gamma, 2) * int(epsilon, 2)


def test_real_input_part1():
    readings = read_input()
    result = part1(readings)
    assert result == 4118544


def part1(readings):
    counts = calculate_counts(readings)
    gamma = calculate_gamma(counts)
    epsilon = calculate_epsilon(counts)
    result = int(gamma, 2) * int(epsilon, 2)
    return result


def calculate_epsilon(counters):
    epsilon = calculate_nth_most_common(counters, -1)
    return epsilon


def calculate_gamma(counters):
    gamma = calculate_most_common(counters)
    return gamma


def calculate_most_common(counters):
    out = ""
    for col in counters:
        val = col.most_common_value()
        out = out + val
    return out


def calculate_least_common(counters):
    out = ""
    for col in counters:
        val = col.least_common_value()
        out = out + val
    return out


class TieBreakCounter(Counter):
    def most_common_value(self, tie_break="1"):
        mc = super(TieBreakCounter, self).most_common()
        if len(mc) > 1 and mc[0][1] == mc[1][1]:
            return tie_break
        return mc[0][0]

    def least_common_value(self, tie_break="0"):
        mc = super(TieBreakCounter, self).most_common()
        mc = mc[::-1]
        if len(mc) > 1 and mc[0][1] == mc[1][1]:
            return tie_break
        return mc[0][0]


def calculate_counts(sample):
    counters = []
    for i in range(len(sample[0])):
        counters.append(TieBreakCounter([x[i] for x in sample]))
    return counters
