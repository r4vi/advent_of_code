from collections import Counter


def parse_input(input_):
    data = []
    with open(input_, 'r') as f:
        data = f.read().strip().splitlines()
    cards = [x.split(': ')[1].strip() for x in data]
    nums_and_winners = [x.split(' | ') for x in cards]
    ret = []
    for nums, winners in nums_and_winners:
        nums = {int(x) for x in nums.strip().split(' ') if x}
        winners = {int(x) for x in winners.strip().split(' ') if x}
        ret.append((nums, winners))
    return ret


def score1(n):
    if n in {0, 1}:
        return n
    return 2 ** (n - 1)


def part1(input_):
    data = parse_input(input_)
    points = 0
    for nums, winners in data:
        matches = nums.intersection(winners)
        score = score1(len(matches))
        points += score
        print(f'{nums=}, {winners=}, {matches=}, {score=}')
    print(f'{points=}')


def part2(input_):
    data = parse_input(input_)
    p2 = [1] * len(data)

    print(f'{p2}')
    for idx, (nums, winners) in enumerate(data):
        matches = nums.intersection(winners)
        num_to_add = len(matches)
        for j in range(num_to_add):
            p2[idx + j + 1] += p2[idx]

    print(f'{p2},\n {sum(p2)}')


if __name__ == '__main__':
    # part1('./input.txt')
    # part2('./sample.txt')
    part2('./input.txt')
