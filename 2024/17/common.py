def run_program(
    a: int,
    b: int,
    c: int,
    prog: list[int],
    debug_print: bool = False,
) -> list[int]:
    # Helper function to get combo operand
    def combo(operand):
        if operand >= 0 and operand <= 3:
            return operand
        if operand == 4:
            return a
        if operand == 5:
            return b
        if operand == 6:
            return c
        if operand == 7:
            raise ValueError("Combo operand 7 is reserved")
        raise RuntimeError(f"Invalid operand: {operand}")

    # Initialize the output
    output = []
    # Initialize the instruction pointer
    pointer = 0
    while True:
        # Halt if we have reached the end of the program
        if pointer >= len(prog):
            break
        # Get the current instruction
        opcode = prog[pointer]
        operand = prog[pointer + 1]

        if debug_print:
            print(
                f"p={pointer:2d}  {a=:<8d}  {b=:<8d}  {c=:<8d} i={opcode} o={operand} c={combo(operand) if operand != 7 else 'n/a'}"
            )

        # Execute the instruction
        if opcode == 0:
            a //= 2 ** combo(operand)
        elif opcode == 1:
            b ^= operand
        elif opcode == 2:
            b = combo(operand) % 8
        elif opcode == 3:
            # if regA is 0, the program will halt
            # otherwise, jump back
            if a != 0:
                pointer = operand
                if debug_print:
                    print("-" * 80)
                continue
        elif opcode == 4:
            b ^= c
        elif opcode == 5:
            if debug_print:
                print(combo(operand) % 8)
            output.append(combo(operand) % 8)
        elif opcode == 6:
            # opcode=6 does not appear in input programs
            b = a // 2 ** combo(operand)
        elif opcode == 7:
            c = a // 2 ** combo(operand)
        else:
            raise RuntimeError(f"Invalid opcode: {opcode}")
        # Jump to the next instruction
        pointer += 2
    return output
