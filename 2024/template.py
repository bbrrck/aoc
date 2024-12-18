# ruff: noqa: F403 F405

import sys

sys.path.insert(0, "../")
from pathlib import Path
from aoc_tools import *

filename = (
    Path(__file__).parent / "input.txt" if len(sys.argv) < 2 else Path(sys.argv[1])
)

with open(filename) as f:
    data = f.read()

# ------------------------------------------------
