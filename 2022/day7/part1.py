import itertools
import os
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint
import sys

sample = """\
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""


def is_int(i):
    try:
        int(i)
        return True
    except ValueError:
        return False


@dataclass
class Node:
    name: str
    type: str
    children: list
    file_size: int
    parent: "Node"

    @property
    def size(self):
        return (
            sum(c.size for c in self.children) if self.type == "dir" else self.file_size
        )

    def flatten(self):
        f_children = []
        if self.children:
            f_children = list(
                itertools.chain.from_iterable([c.flatten() for c in self.children])
            )
        return [self] + f_children

    def __getitem__(self, item):
        try:
            return [x for x in self.children if x.name == item][0]
        except IndexError as ie:
            raise KeyError(item) from ie


def main():
    # part 1
    ## sample
    root = data_to_tree(sample)

    rf = root.flatten()
    sample_sz = sum([x.size for x in rf if x.type == "dir" and x.size <= 100000])
    pprint(f"{sample_sz=}")

    # part 1
    #  input
    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    input_raw = (dir_path / Path("./input")).open("r").read()
    root = data_to_tree(input_raw)

    rf = root.flatten()
    p1_sz = sum([x.size for x in rf if x.type == "dir" and x.size <= 100000])
    pprint(f"{p1_sz=}")

    # part 2
    # find the smallest dir that is > 30000000
    total_disk = 70000000
    free_space = total_disk - root.size
    update_size = 30000000
    req_space = update_size - free_space
    # find smallest dir to delete
    dirs = [(x.name, x.size) for x in rf if x.type == "dir" and x.size < req_space]
    sorted_dirs = sorted(dirs, key=lambda x: x[1])
    pprint(sorted_dirs[0])

    return 0


def data_to_tree(data):
    root = None
    for line in data.splitlines():
        match line.strip().split():
            case ["$", cmd, rest]:
                match rest:
                    case "/":
                        root = Node(
                            name=rest, type="dir", children=[], file_size=0, parent=None
                        )
                        current = root
                    case "..":
                        current = current.parent or root
                    case _:
                        this = Node(
                            name=rest,
                            type="dir",
                            children=[],
                            file_size=0,
                            parent=current,
                        )
                        current.children.append(this)
                        current = this

            case ["$", "ls"]:
                pass
            case ["dir", dirname]:
                pass
            case [size, rest]:
                this = Node(
                    name=rest,
                    type="file",
                    children=[],
                    file_size=int(size),
                    parent=current,
                )
                current.children.append(this)
    return root


if __name__ == "__main__":
    sys.exit(main())
