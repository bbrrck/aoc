import re
import sys
from pathlib import Path

filename = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("input.txt")

with filename.open() as f:
    data = f.read()


def run(regA, regB, regC, program):
    def combo(operand):
        if operand >= 0 and operand <= 3:
            return operand
        if operand == 4:
            return regA
        if operand == 5:
            return regB
        if operand == 6:
            return regC
        if operand == 7:
            raise ValueError(
                "Combo operand 7 is reserved and will not appear in valid programs."
            )
        raise RuntimeError(f"Unknown combo operand {operand}")

    out = []
    pointer = 0
    while True:
        if pointer >= len(program):
            break
        opcode = program[pointer]
        operand = program[pointer + 1]
        if opcode == 0:
            regA //= 2 ** combo(operand)
        elif opcode == 1:
            regB ^= operand
        elif opcode == 2:
            regB = combo(operand) % 8
        elif opcode == 3:
            if regA != 0:
                pointer = operand
                continue
        elif opcode == 4:
            regB ^= regC
        elif opcode == 5:
            out.append(combo(operand) % 8)
        elif opcode == 6:
            regB = regA // 2 ** combo(operand)
        elif opcode == 7:
            regC = regA // 2 ** combo(operand)
        else:
            raise RuntimeError(f"Unknown opcode {opcode}")
        pointer += 2
    return out


regA, regB, regC, program = re.match(
    r"Register A: (\d+)\nRegister B: (\d+)\nRegister C: (\d+)\n\nProgram: (.*)",
    data,
    re.MULTILINE,
).groups()
regA = int(regA)
regB = int(regB)
regC = int(regC)
program = tuple(int(i) for i in program.split(","))


# Part 1
print(*run(regA=regA, regB=regB, regC=regC, program=program), sep=",")
