import pandas as pd

sum_possible, sum_powers = 0, 0
with open("input.txt", "r") as f:
    for line in f.readlines():
        gid, game = line[5:].strip("\n").split(": ")
        df = pd.DataFrame(
            [
                {x.split(" ")[1]: int(x.split(" ")[0]) for x in r.split(", ")}
                for r in game.split("; ")
            ]
        )
        m = df.fillna(0).astype(int).max()
        sum_possible += int(m.red <= 12 and m.green <= 13 and m.blue <= 14) * int(gid)
        sum_powers += m.prod()

print(sum_possible)  # answer 1
print(sum_powers)  # answer 2
