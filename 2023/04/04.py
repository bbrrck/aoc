with open("input.txt", "r") as f:
    lines = f.read().strip("\n").split("\n")

# Part 1
answer_1 = 0  # total score
for line in lines:
    gid, game = line.split(": ")
    winning, mine = game.split(" | ")
    winning = [int(x) for x in winning.split(" ") if x != ""]
    mine = [int(x) for x in mine.split(" ") if x != ""]
    matching = [x for x in mine if x in winning]
    if len(matching) == 0:
        score = 0
    else:
        score = 2 ** (len(matching) - 1)
    answer_1 += score
print(answer_1)

# Part 2
n_cards = [1 for _ in range(len(lines))]
for idx, line in enumerate(lines):
    gid, game = line.split(": ")
    winning, mine = game.split(" | ")
    winning = [int(x) for x in winning.split(" ") if x != ""]
    mine = [int(x) for x in mine.split(" ") if x != ""]
    matching = [x for x in mine if x in winning]
    n_matches = len(matching)
    n_current_card = n_cards[idx]
    for idx_next in range(idx + 1, idx + n_matches + 1):
        if idx_next >= len(lines):
            continue
        n_new_cards = n_current_card
        n_cards[idx_next] += n_new_cards
answer_2 = sum(n_cards)
print(answer_2)
