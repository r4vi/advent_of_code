def main(target):
    input_numbers = []
    with open("./input", "r") as input_file:
        input_values = input_file.readlines()
        input_numbers = [int(x.strip()) for x in input_values]
    for idx, num_x in enumerate(input_numbers):
        for cur, num_y in enumerate(input_numbers):
            for cur_z, num_z in enumerate(input_numbers):
                if idx == cur == cur_z:
                    continue
                if num_x + num_y + num_z == target:
                    print(f"{num_x} + {num_y} == {target}, therefore {num_x} * {num_y} * {num_z} is {num_x * num_y * num_z}")
                    break

if __name__ == '__main__':
    TARGET = 2020
    main(TARGET)
