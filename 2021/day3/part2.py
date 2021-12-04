from part1 import (
    read_input,
    sample,
    calculate_most_common,
    calculate_least_common,
    calculate_counts,
)


def part2(readings):

    i = 0
    oxygen_readings = readings[:]
    while not len(oxygen_readings) == 1:
        counts = calculate_counts(oxygen_readings)
        most_common = calculate_most_common(counts)

        oxygen_readings = [x for x in oxygen_readings if x[i] == most_common[i]]
        i += 1
    print(oxygen_readings)
    oxygen = int(oxygen_readings[0], 2)

    i = 0
    co2_readings = readings[:]
    while not len(co2_readings) == 1:
        counts = calculate_counts(co2_readings)
        least_common = calculate_least_common(counts)

        co2_readings = [x for x in co2_readings if x[i] == least_common[i]]
        i += 1
    print(co2_readings)
    co2 = int(co2_readings[0], 2)
    return oxygen, co2


def test_part2_with_example(sample):
    oxygen, co2 = part2(sample)
    assert oxygen == 23
    assert co2 == 10
    life_support_rating = oxygen * co2

    assert life_support_rating == 230


def test_part2_with_real_input():
    readings = read_input()
    oxygen, co2 = part2(readings)
    assert 3832770 == oxygen * co2
