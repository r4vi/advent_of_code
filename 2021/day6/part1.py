from itertools import repeat
import array

sample_raw = """3,4,3,1,2"""


def parse_input(raw):
    initial_state = map(int, raw.split(","))
    return list(initial_state)


inp = parse_input(sample_raw)


def tick(world):
    new_world = []
    for x in world:
        new_x = x - 1
        if new_x < 0:
            new_world.extend([6, 8])
        else:
            new_world.append(new_x)
    return sorted(new_world)


def world_after_ticks(initial, tick_count):
    tick1 = initial[:]
    for i in range(tick_count):
        tick1 = tick(tick1)
    return len(tick1)


def world_after_ticks_fast(initial, tick_count):
    position_counts = array.array("Q", repeat(0, 8 + 1))
    # set up array with counts
    for i in initial:
        position_counts[i] += 1
    for _ in range(tick_count):
        num_fish_popping = position_counts.pop(0)
        position_counts[6] += num_fish_popping
        position_counts.append(num_fish_popping)
    return sum(position_counts)


def test_sample_steps():
    expected_raw = """Initial state: 3,4,3,1,2
After  1 day:  2,3,2,0,1
After  2 days: 1,2,1,6,0,8
After  3 days: 0,1,0,5,6,7,8
After  4 days: 6,0,6,4,5,6,7,8,8
After  5 days: 5,6,5,3,4,5,6,7,7,8
After  6 days: 4,5,4,2,3,4,5,6,6,7
After  7 days: 3,4,3,1,2,3,4,5,5,6
After  8 days: 2,3,2,0,1,2,3,4,4,5
After  9 days: 1,2,1,6,0,1,2,3,3,4,8
After 10 days: 0,1,0,5,6,0,1,2,2,3,7,8
After 11 days: 6,0,6,4,5,6,0,1,1,2,6,7,8,8,8
After 12 days: 5,6,5,3,4,5,6,0,0,1,5,6,7,7,7,8,8
After 13 days: 4,5,4,2,3,4,5,6,6,0,4,5,6,6,6,7,7,8,8
After 14 days: 3,4,3,1,2,3,4,5,5,6,3,4,5,5,5,6,6,7,7,8
After 15 days: 2,3,2,0,1,2,3,4,4,5,2,3,4,4,4,5,5,6,6,7
After 16 days: 1,2,1,6,0,1,2,3,3,4,1,2,3,3,3,4,4,5,5,6,8
After 17 days: 0,1,0,5,6,0,1,2,2,3,0,1,2,2,2,3,3,4,4,5,7,8
After 18 days: 6,0,6,4,5,6,0,1,1,2,6,0,1,1,1,2,2,3,3,4,6,7,8,8,8,8"""

    expected_raw.split("\n")
    initial = parse_input(sample_raw)
    iterations = [
        sorted(list(map(int, y[1].strip().split(","))))
        for y in [x.split(":") for x in expected_raw.split("\n")[1:]]
    ]

    tick1 = initial[:]
    for i in range(18):
        tick1 = tick(tick1)
        assert tick1 == iterations[i]
    assert world_after_ticks(initial, 18) == 26
    assert world_after_ticks(initial, 80) == 5934


def test_sample_part2():
    initial = parse_input(sample_raw)
    assert world_after_ticks_fast(initial, 18) == 26
    assert world_after_ticks_fast(initial, 80) == 5934
    assert world_after_ticks_fast(initial, 256) == 26984457539


def test_input_part1():
    with open("./input", "r") as i:
        initial = parse_input(i.read())
        assert 365862 == world_after_ticks(initial, 80)
        assert 365862 == world_after_ticks_fast(initial, 80)


def test_input_part2():
    with open("./input", "r") as i:
        initial = parse_input(i.read())
        print(world_after_ticks_fast(initial, 256))
