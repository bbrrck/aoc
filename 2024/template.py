import sys
from pathlib import Path

filename = Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else sys.argv[1]

with open(filename) as f:
    data = f.read()  # noqa: F841

# ------------------------------------------------

...

# ------------------------------------------------

answer_1 = ...
print(answer_1)

# ------------------------------------------------

answer_2 = ...
print(answer_2)

# ------------------------------------------------
