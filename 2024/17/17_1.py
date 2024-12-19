import re
import sys
from pathlib import Path
from common import run_program

filename = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input.txt")
a, b, c, *prog = map(int, re.findall(r"(\d+)", filename.open().read()))

# Part 1
print(*run_program(a, b, c, prog, True), sep=",")
