import math, re


def parse(filename):
    lines, graph = open(filename).read().split("\n"), {}
    for l in lines[2:]:
        a, b, c = re.findall(r"\w{3}", l)
        graph[a] = (b, c)
    return lines[0], graph


def part1(moves, graph):
    pos, c = "AAA", 0
    while pos != "ZZZ":
        pos, c = graph[pos][moves[c % len(moves)] == "R"], c + 1
    return c


def part2(moves, graph):
    a_nodes, cycles = [n for n in graph if n.endswith("A")], []
    for n in a_nodes:
        c = 0
        while not n.endswith("Z"):
            n = graph[n][moves[c % len(moves)] == "R"]
            c += 1
        cycles.append(c)
    return math.lcm(*cycles)


moves, graph = parse("./input.txt")
print(part2(moves, graph))
