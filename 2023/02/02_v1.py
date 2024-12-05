from collections import defaultdict

with open("input.txt", "r") as f:
    contents = f.read()
lines = contents.strip("\n").split("\n")

LIMITS = {"red": 12, "green": 13, "blue": 14}


def is_game_possible(line):
    game = defaultdict(list)
    for subgame in line.split(": ")[-1].split("; "):
        for amount_and_color in subgame.split(", "):
            amount, color = amount_and_color.split(" ")
            amount = int(amount)
            game[color].append(amount)
    is_possible = True
    power = 1
    for color, amounts in game.items():
        max_amount = max(amounts)
        limit_amount = LIMITS[color]
        is_color_possible = max_amount <= limit_amount
        is_possible &= is_color_possible
        power *= max_amount
    return is_possible, power


sum_possible = 0
sum_powers = 0
for idx, line in enumerate(lines):
    gid = idx + 1
    is_possible, power = is_game_possible(line)
    sum_powers += power
    if is_possible:
        sum_possible += gid

answer_1 = sum_possible
answer_2 = sum_powers

print(answer_1)
print(answer_2)
