from typing import List
from collections import OrderedDict
import re

import math


def parse(input_):
    with open(input_, 'r') as f:
        lines: List[str] = f.read().strip().splitlines()
    time, dist = lines
    time = list(map(int, re.findall(r'\d+', time.split('Time:')[1])))
    dist = list(map(int, re.findall(r'\d+', dist.split('Distance:')[1])))
    return OrderedDict(zip(time, dist))

def parse2(input_):
    with open(input_, 'r') as f:
        lines: List[str] = f.read().strip().splitlines()
    time, dist = lines
    time = int(''.join(re.findall(r'\d+', time.split('Time:')[1])))
    dist = int(''.join(re.findall(r'\d+', dist.split('Distance:')[1])))
    return time, dist

def part1(input_):
    races = parse(input_)
    # races is an ordered dict e.g.
    # OrderedDict([(7, 9), (15, 40), (30, 200)])
    all_possible = []
    for race_time, race_dist in races.items():
        possible = []
        print(race_time, race_dist)
        for hold_time in range(race_time + 1):
            travel_time = race_time - hold_time
            distance = hold_time * travel_time
            if distance > race_dist:
                possible.append(hold_time)
        all_possible.append(len(possible))
    print(all_possible)
    print(math.prod(all_possible))

def part2(input_):
    race_time, race_dist = parse2(input_)
    # races is an ordered dict e.g.
    # OrderedDict([(7, 9), (15, 40), (30, 200)])
    possible = 0
    print(race_time, race_dist)
    for hold_time in range(race_time + 1):
        travel_time = race_time - hold_time
        distance = hold_time * travel_time
        if distance > race_dist:
            possible += 1
    print(f'{possible=}')

if __name__ == '__main__':
    # part1('./sample.txt')
    # part1('./input.txt')
    # part2('./sample.txt')
    part2('./input.txt')
