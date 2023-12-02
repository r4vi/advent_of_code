from collections import defaultdict
import math


def parse_input(file_):
    games = []
    with open(file_, 'r') as f:
        games = f.readlines()
    games = [
        l.strip().split(': ')[1].strip().split('; ')
        for l
        in games
    ]
    game_phases = [
        [
            dict([(y.split(' ')[1], int(y.split(' ')[0])) for y in round.split(', ')])
            for round in phase
        ]
        for phase in games
    ]

    return game_phases


def part1(in_):
    """
    The Elf would first like to know which games would
    have been possible if the bag contained only
    12 red cubes, 13 green cubes, and 14 blue cubes?
    """
    possible_game_ids = []
    bag = {
        'red': 12,
        'green': 13,
        'blue': 14
    }
    for idx, game in enumerate(in_, 1):
        print(idx, game)
        possible = True
        for phase in game:
            for colour, count in phase.items():
                if count > bag[colour]:
                    possible = False
                    continue
        if possible:
            possible_game_ids.append(idx)
    print(possible_game_ids)
    print(sum(possible_game_ids))


def part2(in_):
    minimums = []
    for idx, game in enumerate(in_, 1):
        minimum_bag = defaultdict(lambda: 0)

        for phase in game:
            for colour, count in phase.items():
                if count > minimum_bag[colour]:
                    minimum_bag[colour] = count
        minimums.append(dict(minimum_bag))
        print(idx, dict(minimum_bag), game)
    print(minimums)
    print(sum([math.prod(x.values()) for x in minimums]))


if __name__ == '__main__':
    part2(parse_input('./input.txt'))
