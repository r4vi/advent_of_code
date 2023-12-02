import string
from pprint import pprint
from collections import OrderedDict
import re


def part1():
    lines = parse_input()

    trans = str.maketrans({k: None for k in string.ascii_lowercase})
    out = [str.translate(line.strip(), trans) for line in lines]
    first_and_last = [int(''.join([line[0], line[-1]])) for line in out]

    pprint(sum(first_and_last))


def parse_input():
    lines = []
    with open('input.txt', 'r') as p1_input:
        lines = p1_input.readlines()
    return lines


def part2():
    lines = parse_input()

    nmap = OrderedDict({
        'nine': 9,
        '9': 9,
        'eight': 8,
        '8': 8,
        'seven': 7,
        '7': 7,
        'six': 6,
        '6': 6,
        'five': 5,
        '5': 5,
        'four': 4,
        '4': 4,
        'three': 3,
        '3': 3,
        'two': 2,
        '2': 2,
        'one': 1,
        '1': 1
    })
    res = []
    for line in lines:
        line = line.strip()
        left, right = calc(line, nmap)
        res.append(int(f'{left}{right}'))
    pprint(list(zip(res, lines)))
    pprint(sum(res))


def calc(line, nmap):
    lowest_pos = 9999
    highest_pos = -1
    left = 0
    right = 0
    for k, v in nmap.items():
        pos = line.find(k)
        if -1 < pos < lowest_pos:
            lowest_pos = pos
            left = v
        rpos = line.rfind(k)
        if rpos > highest_pos:
            highest_pos = rpos
            right = v
    return left, right


if __name__ == '__main__':
    part2()
