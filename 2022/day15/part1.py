import os
import re
from collections import namedtuple
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


def apply_move(start, move):
    return Point(start.x + move.x, start.y + move.y)


for line in input_raw.splitlines():
    coords = re.findall(COORDS_RE, line)
    coords = list(map(int, coords))
    sx, sy, bx, by = coords
    sensor = Point(sx, sy)
    beacon = Point(bx, by)
    d = SensorAndBeacon(sensor, beacon)
    data.append(d)

UP = Point(0, -1)
DOWN = Point(0, 1)
LEFT = Point(-1, 0)
RIGHT = Point(1, 0)
UP_LEFT = Point(-1, -1)
DOWN_LEFT = Point(-1, 1)
DOWN_RIGHT = Point(1, 1)
UP_RIGHT = Point(1, -1)

MOVES = [UP, DOWN, LEFT, RIGHT, UP_LEFT, UP_RIGHT, DOWN_LEFT, DOWN_RIGHT]


def get_adj(p):
    return {apply_move(p, m) for m in MOVES}


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

for s, kb in data:
    dist_b = manhattan_distance(s, kb)
    y = 2000000
    for x in range(s.x - dist_b - 1, s.x + dist_b + 1):
        dist_p = manhattan_distance(s, p := Point(x, y))
        if dist_p <= dist_b and p not in beacon_locs:
            no_beacon.add(p)

# print_coord_map(sensor_locs, beacon_locs, no_beacon)
y10 = [x for x in no_beacon if x.y == 2000000]
print(len(y10))
