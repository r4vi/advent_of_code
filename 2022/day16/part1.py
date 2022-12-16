import os
import random
import re
from collections import deque, Counter
from dataclasses import dataclass
from operator import attrgetter
import heapq
from pathlib import Path
from pprint import pprint
from typing import NamedTuple

from loguru import logger
import sys

logger.remove()
logger.add(sys.stderr, level="INFO")

sample = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II"""


dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

input_raw = (dir_path / Path("./input")).open("r").read()

EXTRACT_RE = re.compile(
    r"Valve (?P<valve>\w+) has flow rate=(?P<rate>\d+); tunnels? lead(s)? to valves? (?P<outputs>.+)"
)


class Instruction(NamedTuple):
    valve: str
    rate: int


nodes = {}
edges: dict[str:Instruction] = {}

for line in input_raw.splitlines():
    m = re.search(EXTRACT_RE, line)
    gd = m.groupdict()
    i = Instruction(valve=gd["valve"], rate=int(gd["rate"]))
    edges[i.valve] = set(gd["outputs"].split(", "))
    nodes[i.valve] = i

# hint from https://github.com/davearussell/advent2022/blob/master/day16/solve.py
for name, neighbours in list(edges.items()):
    del edges[name]
    edges[nodes[name]] = {nodes[neighbour]: 1 for neighbour in neighbours}


def find_paths(edges, goal):
    q = [(0, goal)]
    path_lengths = {goal: 0}
    while q:
        cost, current = heapq.heappop(q)
        for point, point_cost in edges[current].items():
            if point not in path_lengths or cost + point_cost < path_lengths[point]:
                path_lengths[point] = cost + point_cost
                heapq.heappush(q, (cost + point_cost, point))
    return path_lengths


def find_all_paths(edges, start_node):
    costs = {
        node: find_paths(edges, node)
        for node in edges
        if node is start_node or node.rate
    }
    for node, node_costs in costs.items():
        costs[node] = {x: c for x, c in node_costs.items() if x.rate}
    return costs


def run_order(costs, start_node, nodes, t):
    release = 0
    current = start_node
    for node in nodes:
        cost = costs[current][node] + 1
        t -= cost
        assert t > 0
        release += t * node.rate
        current = node
    return release


def all_orders(distances, node, todo, done, time):
    for next_node in todo:
        cost = distances[node][next_node] + 1
        if cost < time:
            yield from all_orders(
                distances,
                next_node,
                todo - {next_node},
                done + [next_node],
                time - cost,
            )
    yield done


pprint(nodes)
start_node = nodes["AA"]
distances = find_all_paths(edges, start_node)
working_nodes = {node for node in distances if node.rate}

p1_orders = all_orders(distances, start_node, working_nodes, [], 30)
best_value = max(run_order(distances, start_node, order, 30) for order in p1_orders)
print("Part 1:", best_value)

p2_orders = all_orders(distances, start_node, working_nodes, [], 26)
p2_scores = [
    (run_order(distances, start_node, order, 26), set(order)) for order in p2_orders
]
p2_scores.sort(key=lambda x: -x[0])

best = 0
for i, (sa, oa) in enumerate(p2_scores):
    if sa * 2 < best:
        break
    for sb, ob in p2_scores[i + 1 :]:
        if not oa & ob:
            score = sa + sb
            if score > best:
                best = score
print("Part 2:", best)
