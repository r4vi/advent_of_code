from pathlib import Path

# generated by openai - minimal changes to the prompt, today it fails


def calculate_total_score(strategy_guide):
    total_score = 0
    for line in strategy_guide:
        opponent_shape, player_shape = line.split()
        opponent_score = 0
        player_score = 0
        if opponent_shape == "A":
            opponent_score = 1
        elif opponent_shape == "B":
            opponent_score = 2
        elif opponent_shape == "C":
            opponent_score = 3
        if player_shape == "X":
            player_score = 1
        elif player_shape == "Y":
            player_score = 2
        elif player_shape == "Z":
            player_score = 3
        if opponent_score == player_score:
            total_score += 6
        elif (
            (opponent_score == 1 and player_score == 2)
            or (opponent_score == 2 and player_score == 3)
            or (opponent_score == 3 and player_score == 1)
        ):
            total_score += 8
        else:
            total_score += 1
    return total_score


if __name__ == "__main__":
    guide = Path("./sample").open("r").readlines()
    ts = calculate_total_score(guide)
    print(ts)
    guide = Path("./input").open("r").readlines()
    ts = calculate_total_score(guide)
    print(ts)  # wrong
