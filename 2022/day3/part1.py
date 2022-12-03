import sys, os
import string
from pathlib import Path

sample = \
"""vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

PRIORITY = { letter: i+1  for i, letter in enumerate(string.ascii_letters) }

def process_input(input_):
    intersections = []
    for line in input_:
        line_len = len(line)
        mid = line_len // 2
        c1, c2 = line[:mid], line[mid:]
        print(f"{c1=}, {c2=}")
        unique_c1, unique_c2 = set(c1), set(c2)
        in_both_compartments = list(unique_c1 & unique_c2)
        intersections.append(PRIORITY[in_both_compartments[0]])
        print(f"{intersections=}")
        print(f"sum intersections: {sum(intersections)}")
def main():
    # part 1
    ## sample
    process_input(sample.split())
   

    ## with input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))

    input_raw = (dir_path / Path('./input')).open('r').read()
    process_input(input_raw.split())

    return 0
if __name__ == '__main__':
    sys.exit(main())