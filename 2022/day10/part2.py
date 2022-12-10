from dataclasses import dataclass
import os
from pathlib import Path
from pprint import pprint
import sys
from collections import deque

sample = """\
noop
addx 3
addx -5"""

sample2 = """\
addx 15
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


@dataclass(kw_only=True)
class Instruction:
    name: str
    width: int
    ticks: int = 0

    @property
    def complete(self):
        return not (self.ticks < self.width)

    def apply(self, registers):
        if self.ticks < self.width:
            self.ticks += 1
        else:
            self.run(registers)

    def run(self, registers):
        raise NotImplementedError()


@dataclass(kw_only=True)
class AddX(Instruction):
    x: int
    name: str = "addx"
    width: int = 2

    def run(self, registers):
        registers[0] += self.x


@dataclass(kw_only=True)
class Noop(Instruction):
    name: str = "noop"
    width: int = 1

    def run(self, registers):
        pass


def calculate2(instructions):
    inst_q = deque()
    for inst in instructions.splitlines():
        match inst.split():
            case ["noop"]:
                # print("noop")
                inst_q.append(Noop())
            case ["addx", x]:
                x = int(x)
                # print(f"addx {x}")
                inst_q.append(AddX(x=x))
    return inst_q


def run_clock(program, registers):

    while program:
        curr = program[0]
        curr.apply(registers)
        yield registers
        if curr.complete:
            curr.apply(registers)
            program.popleft()


def main():

    sigpos = list(range(40, 260, 40))

    # part 2

    ## sample2
    prog = calculate2(sample2)
    registers = r = [1]
    register_generator = run_clock(prog, registers)
    row = list("." * 40)
    for i in range(sigpos[-1] + 1):

        try:
            r = next(register_generator)
        except StopIteration:
            print("".join(row))
            break
        sprite_pos = r[0]
        row_idx = i % 40
        if row_idx in range(sprite_pos - 1, sprite_pos + 2):
            # if current pixel is within a sprite

            row[row_idx] = "#"

        if i in sigpos:
            print("".join(row))
            row = list("." * 40)

    # part 1
    ## input
    print()
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()
    prog = calculate2(input_raw)
    registers = r = [1]
    register_generator = run_clock(prog, registers)
    row = list(" " * 40)
    for i in range(sigpos[-1] + 1):

        try:
            r = next(register_generator)
        except StopIteration:
            print("".join(row))
            break
        sprite_pos = r[0]
        row_idx = i % 40
        if row_idx in range(sprite_pos - 1, sprite_pos + 2):
            # if current pixel is within a sprite

            row[row_idx] = "#"

        if i in sigpos:
            print("".join(row))
            row = list(" " * 40)
    return 0


if __name__ == "__main__":
    sys.exit(main())
