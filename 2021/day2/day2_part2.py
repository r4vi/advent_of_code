from dataclasses import dataclass

import pytest


@dataclass
class Submarine:
    x: int = 0  # x is forward / backwards
    y: int = 0  # y is inverted, - is up / + down
    aim: int = 0


def forward(sub: Submarine, arg: int) -> Submarine:
    sub.x += arg
    sub.y += sub.aim * arg
    return sub


def up(sub: Submarine, arg: int) -> Submarine:
    sub.aim -= arg
    return sub


def down(sub: Submarine, arg: int) -> Submarine:
    sub.aim += arg
    return sub


COMMANDS = {"forward": forward, "up": up, "down": down}


def read_input(input_file="./input"):
    with open(input_file, "r") as input:
        return [x.strip() for x in input.readlines()]


def parse_line(line):
    command, arg = line.split()
    return [COMMANDS[command], int(arg)]


def parse_input(input):
    return [parse_line(line) for line in input]


def execute_lines(lines, sub: Submarine):
    for command, arg in lines:
        command(sub, arg)
    return sub


def part_two(values) -> int:
    lines = parse_input(values)
    sub = Submarine(0, 0, 0)
    execute_lines(lines, sub)
    return sub.x * sub.y


@pytest.fixture
def sample():
    return ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"]


def test_sample_input_part_two(sample):
    assert part_two(sample) == 900


def test_real_input_part_two():
    input = read_input()
    assert part_two(input) == 1963088820
