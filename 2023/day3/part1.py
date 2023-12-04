import string
from collections import defaultdict
from math import prod
from typing import List, Generator


def adjacent_8(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for y_d in (-1, 0, 1):
        for x_d in (-1, 0, 1):
            if y_d == x_d == 0:
                continue
            yield x + x_d, y + y_d


def parse_input(_in) -> List[str]:
    ret = None
    with open(_in, 'r') as f:
        ret = f.read().strip().splitlines()
    return ret


def print_grid(g):
    for row in g:
        for col in row:
            print(col, end='')
        print('')


def get_coord(g, x, y):
    try:
        return g[y][x]
    except IndexError:
        return '.'


def part1(input_):
    NON_SYMBOL = set(string.digits + '.')
    data = parse_input(input_)
    print_grid(data)
    part_numbers = []
    for y, v in enumerate(data):
        parsing_digit = ''
        adjs = set()
        for x, c in enumerate(v):
            if c.isdigit():
                parsing_digit += c
                adjs.update(set(adjacent_8(x, y)))
            else:
                if parsing_digit:
                    found_vals = set()
                    for loc in adjs:
                        found_vals.add(get_coord(data, *loc))
                    if found_vals - NON_SYMBOL:
                        part_numbers.append(int(parsing_digit))
                    parsing_digit = ''
                    adjs = set()
        # ugly; handle end of line
        if parsing_digit:
            found_vals = set()
            for loc in adjs:
                found_vals.add(get_coord(data, *loc))
            if found_vals - NON_SYMBOL:
                part_numbers.append(int(parsing_digit))

    print(part_numbers)
    print(sum(part_numbers))


def part2(input_):
    data = parse_input(input_)
    print_grid(data)
    stars_and_adj_digit_dict = defaultdict(list)
    for y, v in enumerate(data):
        parsing_digit = ''
        adjs = set()
        for x, c in enumerate(v):
            if c.isdigit():
                parsing_digit += c
                adjs.update(set(adjacent_8(x, y)))
            else:
                if parsing_digit:
                    for loc in adjs:
                        loc_val = get_coord(data, *loc)
                        if loc_val == '*':
                            stars_and_adj_digit_dict[loc].append(int(parsing_digit))
                    parsing_digit = ''
                    adjs = set()
        # ugly; handle end of line
        if parsing_digit:
            for loc in adjs:
                loc_val = get_coord(data, *loc)
                if loc_val == '*':
                    stars_and_adj_digit_dict[loc].append(int(parsing_digit))

    print(stars_and_adj_digit_dict)
    print(sum([prod(g) for g in stars_and_adj_digit_dict.values() if len(g) == 2]))

if __name__ == '__main__':
    # part1('./input.txt')
    part2('./input.txt')
