def parse_input(file_name):
    elves = []
    with open(file_name, "r") as input:
        current_elf = []
        for line in input.readlines():
            if l := line.strip():
                current_elf.append(int(l))
            else:
                elves.append(current_elf)
                current_elf = []
    return elves


if __name__ == "__main__":
    elf_calories = parse_input("./input")
    elf_sorted = sorted([sum(x) for x in elf_calories])
    print(sum(elf_sorted[-3:]))
