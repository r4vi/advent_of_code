from itertools import combinations

def main(target):
    input_numbers = []
    with open("./input", "r") as input_file:
        input_values = input_file.readlines()
        input_numbers = [int(x.strip()) for x in input_values]
    possible_triples = combinations(input_numbers, 3)
    for num_x, num_y, num_z in possible_triples:
        if num_x + num_y + num_z == target:
            print(f"{num_x} + {num_y} == {target}, therefore {num_x} * {num_y} * {num_z} is {num_x * num_y * num_z}")

if __name__ == '__main__':
    TARGET = 2020
    main(TARGET)
