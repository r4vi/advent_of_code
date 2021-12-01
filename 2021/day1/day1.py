import sys


def parse_input(file_name):
    with open(file_name, "r") as input:
        return [int(x.strip()) for x in input.readlines() if x.strip()]


def calculate(values):
    output = []
    for idx, cur in enumerate(values):
        if idx == 0:
            output.append(False)
            continue
        print(f"checking if {cur} > {values[idx-1]}")
        output.append(cur > values[idx - 1])
    print(list(zip(values, output)))
    print(f"number of increases: {len([x for x in output if x])}")


def calculate_part_2(values, win_size=3):
    output = []
    old_window_sum = sys.maxsize
    for i in range(len(values) - win_size + 1):

        window = values[i : i + win_size]
        cur_window_sum = sum(window)
        print(window, cur_window_sum)

        if i == 0:
            output.append(False)
        else:
            output.append(cur_window_sum > old_window_sum)

        old_window_sum = cur_window_sum
    print(output)
    print(f"number of increases: {len([x for x in output if x])}")


if __name__ == "__main__":
    v = parse_input("./input")
    calculate(v)
    calculate_part_2(v)
