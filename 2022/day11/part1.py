import operator
import os
import re
from collections import deque
from pathlib import Path
from pprint import pprint, pformat
import sys

sample = """Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1"""

OP_MAP = {
    "*": operator.mul,
    "-": operator.sub,
    "+": operator.add,
    "/": operator.truediv,
}


def main():
    # part 1
    ## sample
    monkeys = sample.split("\n\n")

    # play a round
    round = to_round(monkeys)
    mb = run_game(round)
    pprint(mb)
    mb = sorted(mb.items(), key=operator.itemgetter(1), reverse=True)
    print(
        f"top inspecting monkeys are {mb[:2]}, their total monkey business is: {mb[0][1]*mb[1][1]}"
    )

    # part 1
    ## input

    dir_path = Path(os.path.dirname(os.path.realpath(__file__)))
    input_raw = (dir_path / Path("./input")).open("r").read()
    round = to_round(input_raw.split("\n\n"))
    mb = run_game(round)
    pprint(mb)
    mb = sorted(mb.items(), key=operator.itemgetter(1), reverse=True)
    print(
        f"top inspecting monkeys are {mb[:2]}, their total monkey business is: {mb[0][1]*mb[1][1]}"
    )
    return 0


def run_game(round):
    for n in range(1, 21):
        for monkey in round:
            print(f"Monkey {monkey['id']}:")
            for item in monkey["items"].copy():
                print(f"\tMonkey inspects an item with worry level of {item}")
                monkey["inspected"] += 1
                mutated = monkey["mutate"](item)
                print(f"\t\tWorry level is {monkey['op']} to {mutated}")
                new = mutated // 3
                print(
                    f"\t\tMonkey gets bored with item. Worry level is divided by 3 to {new}."
                )
                is_divisible = monkey["test"](new)
                txt_is_div = "is" if is_divisible else "is not"
                print(
                    f"\t\tCurrent worry level {txt_is_div} divisible by {monkey['div_check']}."
                )
                destination_monkey = monkey[is_divisible]
                round[destination_monkey]["items"].append(new)
                monkey["items"].popleft()
                print(
                    f"\t\tItem with worry level {new} is thrown to monkey {destination_monkey}."
                )
        pprint(f"Round {n} = " + pformat({m["id"]: m["inspected"] for m in round}))
        for monkey in round:
            print(f"Monkey {monkey['id']}: {', '.join(map(str, monkey['items']))}")
        print("")
    return {m["id"]: m["inspected"] for m in round}


def fix_operand(operand, old):
    match operand:
        case "old":
            return old
        case _:
            return int(operand)


def to_round(monkeys):
    round = []
    for monkey in monkeys:
        monkey_id, initial_state, op, test, if_true, if_false = [
            x.strip() for x in monkey.splitlines()
        ]
        monkey_id = int(monkey_id.rstrip(":").split()[1])
        initial_state = deque(
            [
                int(y)
                for y in [x.strip() for x in initial_state.split(":")][1].split(",")
            ]
        )
        op_l, op_f, op_r = re.findall(r"old.*", op)[0].split()

        def mutate_maker(op_l, op_f, op_r):
            def inner(old):
                op_l_ = fix_operand(op_l, old)
                op_r_ = fix_operand(op_r, old)

                return OP_MAP[op_f](op_l_, op_r_)

            return inner

        div_check = int(re.findall(r"\d+$", test)[0])

        def test_maker(div_check):
            def inner(x):
                return (x % div_check) == 0

            return inner

        test = test_maker(div_check)

        if_true = int(if_true[-1])
        if_false = int(if_false[-1])
        round.append(
            {
                "id": monkey_id,
                "items": initial_state,
                "mutate": mutate_maker(op_l, op_f, op_r),
                "op": (op_l, op_f, op_r),
                "test": test,
                "div_check": div_check,
                True: if_true,
                False: if_false,
                "inspected": 0,
            }
        )
    return round


if __name__ == "__main__":
    sys.exit(main())
    pass
