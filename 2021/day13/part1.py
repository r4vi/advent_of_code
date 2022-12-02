from collections import Counter
from itertools import chain

sample_raw = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"""

def print_grid(grid):
    max_x = max([x[0] for x in grid])
    max_y = max([x[1] for x in grid])
    xs = '\t'.join([str(x) for x in range(max_x+1)])
    print(f"{xs}")
    for y in range(max_y+1):
        for x in range(max_x+1):
            if [x, y,] in grid:
                print('#', end="\t")
            else:
                print('.', end="\t")

        print(f"\t: y={y}")

def parse_input(raw):
    grid, folds = raw.split("\n\n")
    grid = grid.split()
    grid = [[int(x), int(y)] for x,y in [x.split(",") for x in grid]]
    folds = folds.strip().split("\n")
    folds = [x.strip("fold along ").split("=") for x in folds]
    folds = [[f[0], int(f[1])] for f in folds]
    return grid, folds


def fold_grid(grid_source, at_axis, offset):
    if at_axis == 'x':
        axis = 0
    else:
        axis = 1

    grid_a = []
    grid_b = []
    max_axis = max(coord[axis] for coord in grid_source)
    for coord in grid_source:
        coord = coord[:]
        if coord[axis] >= offset:
            coord[axis] = max_axis - coord[axis]
            grid_b.append(coord)
        else:
            grid_a.append(coord)
    return grid_a, grid_b
    # print_grid(grid_a)
    # print_grid(grid_b)

def count_dots(*grids):
    return len(set(tuple(c) for c in chain.from_iterable(grids)))

def test_fold_grid_y():
    grid, folds = parse_input(sample_raw)
    print_grid(grid)
    a, b = fold_grid(grid, "y", 7)
    print_grid(a)
    print_grid(b)
    print_grid(a+b)
    assert count_dots(a, b) == 17

def test_fold_grid_x():
    grid, folds = parse_input(sample_raw)
    print_grid(grid)
    a, b = fold_grid(grid, "x", 5)
    print_grid(a)
    print_grid(b)
    print_grid(a+b)
    assert count_dots(a, b) == 17

def test_fold_grid_x_y():
    grid, folds = parse_input(sample_raw)
    print_grid(grid)
    a1, b1 = fold_grid(grid, "y", 7)
    print_grid(a1)
    print_grid(b1)
    print_grid(a1+b1)
    a2, b2 = fold_grid(a1+b1, "x", 5)
    print_grid(a2)
    print_grid(b2)
    print_grid(a2+b2)
    assert count_dots(a2, b2) == 16

def test_input_part1():
    with open('./input', 'r') as i:
        grid, folds = parse_input(i.read())
        a = grid
        b = []
        for fold in folds:
            a, b = fold_grid(a+b, *fold)
            print(f"fold: {fold} \t count: {count_dots(a, b)}")
            # print_grid(a+b)
