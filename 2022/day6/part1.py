import os
from pathlib import Path
from pprint import pprint
import sys

sample = """mjqjpqmgbljsphdztnvjfqwrcgsmlb"""


def main():

    # part 1
    ## sample
    for offset in range(len(sample)):
        marker = set(sample[offset : offset + 4])
        if len(marker) == 4:
            print(f"{offset+4=}: {marker=}")
            break

    # part 1
    ## input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path("./input")).open("r").read()
    for offset in range(len(input_raw)):
        marker = set(input_raw[offset : offset + 4])
        if len(marker) == 4:
            print(f"{offset+4=}: {marker=}")
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
