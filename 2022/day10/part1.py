from operator import itemgetter
import os
from pathlib import Path
from pprint import pprint
import sys
from collections import deque

sample = """noop
addx 3
addx -5"""

sample2 = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop"""

def calculate(instructions):

    register_x = 1
    expanded = []

    for inst in instructions.splitlines():
    
        match inst.split():
            case ["noop"]:
                print('noop')
                expanded.append(0)
            case ["addx", x]:
                x = int(x)
                print(f"addx {x}")
                expanded.extend([0, x])
        
    return expanded

def main():

    # part 1
    ## sample
    xs = calculate(sample)
    assert sum(xs) + 1 == -1
    
    sigpos = [20,60,100,140,180,220]
    ## sample2
    xs = calculate(sample2)
    assert (sum(xs[0:20]) + 1) * 20 == 420
    assert (sum(xs[0:60]) + 1) * 60 == 1140
    sigv =    [(sum(xs[0:pos])+1) * pos for pos in sigpos]
    assert sum(sigv) == 13140




    # part 1
    ## input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()
    xs = calculate(input_raw)
    
    sigv=    [(sum(xs[0:pos])+1) * pos for pos in sigpos]
    return 0


if __name__ == "__main__":
    sys.exit(main())
