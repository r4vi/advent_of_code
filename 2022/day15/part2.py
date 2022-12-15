import os
import re
from collections import namedtuple, defaultdict
from pathlib import Path
from typing import Iterable
import math

sample = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

COORDS_RE = re.compile(r"(?<=[xy]=)-?\d+")

data = []
Point = namedtuple("Point", "x y")
SensorAndBeacon = namedtuple("SensorAndBeacon", "sensor beacon")


dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

input_raw = (dir_path / Path("./input")).open("r").read()


for line in input_raw.splitlines():
    coords = re.findall(COORDS_RE, line)
    coords = list(map(int, coords))
    sx, sy, bx, by = coords
    sensor = Point(sx, sy)
    beacon = Point(bx, by)
    d = SensorAndBeacon(sensor, beacon)
    data.append(d)


def print_coord_map(sensors: set[Point], beacons: set[Point], nots: set[Point]):
    all_points = sensors | beacons | nots
    min_x = min(c.x for c in all_points)
    min_y = min(c.y for c in all_points)
    max_x = max(c.x for c in all_points)
    max_y = max(c.y for c in all_points)

    for yy in range(min_y, max_y + 1):
        print(f"{yy:3}\t", end="")
        for xx in range(min_x, max_x + 1):
            val = "#" if Point(xx, yy) in nots else "."
            val = "S" if Point(xx, yy) in sensors else val
            val = "B" if Point(xx, yy) in beacons else val
            print(f"{val:2}", end="")
        print("")


sensor_locs = set()
no_beacon = set()
beacon_locs = set()


for sensor, known_beacon in data:
    print(known_beacon)
    sensor_locs.add(sensor)
    beacon_locs.add(known_beacon)


def manhattan_distance(p1, p2):
    return abs(p2.x - p1.x) + abs(p2.y - p1.y)


all_points = sensor_locs | beacon_locs
min_x = min(c.x for c in all_points)
min_y = min(c.y for c in all_points)
max_x = max(c.x for c in all_points)
max_y = max(c.y for c in all_points)
search_space = set()

max_coord = 4000000
# max_coord = 20

diamond_edges = defaultdict(int)

beacon_and_sensor_locs = beacon_locs | sensor_locs

for s, kb in data:
    dist_b = manhattan_distance(s, kb)
    print(f"checking {s}")
    y_start = max(0, s.y - dist_b)
    y_end = min(s.y + dist_b, max_coord) + 1

    for y in range(y_start, y_end):
        x_start = max(0, s.x - dist_b)
        x_end = min(s.x + dist_b + 1, max_coord)
        for x in range(x_start, x_end):
            dist_p = abs(x - s.x) + abs(y - s.y)
            if dist_p == dist_b + 1:
                p = Point(x,y)
                if p not in beacon_and_sensor_locs:
                    diamond_edges[p] += 1

# print_coord_map(sensor_locs, beacon_locs, no_beacon)
poss = [k for k,v in diamond_edges.items() if v == max(diamond_edges.values())]
print((poss[-1].x*4000000) + poss[-1].y)
