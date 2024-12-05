with open("input.txt", "r") as f:
    contents = f.read()
lines = contents.split("\n")

# ----------------------------------------
# Part 1
# ----------------------------------------

answer_1 = 0
numbers = [str(y) for y in range(10)]
for line in lines:
    number = ""
    for x in line:
        if x in numbers:
            number += x
    if number == "":
        continue
    if len(number) == 1:
        number += number
    if len(number) > 2:
        number = number[0] + number[-1]
    number = int(number)
    answer_1 += number
print(answer_1)

# ----------------------------------------
# Part 2
# ----------------------------------------

NUMBERS = [
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine",
]


def find_left_digit(line):
    _pos = 1_000_000_000
    _digit = None

    for digit, word in enumerate(NUMBERS):
        digit = str(digit)

        # find the leftmost occurence of the number word
        # save it if it occurs before the previously found leftmost number
        pos_w = line.find(word)
        if pos_w > -1 and pos_w < _pos:
            _pos = pos_w
            _digit = digit

        # find the leftmost occurence of the number digit
        # save it if it occurs before the previously found leftmost number
        pos_d = line.find(digit)
        if pos_d > -1 and pos_d < _pos:
            _pos = pos_d
            _digit = digit

    return _digit


def find_right_digit(line):
    _pos = -1_000_000_000
    _digit = None

    for digit, word in enumerate(NUMBERS):
        digit = str(digit)

        # find the rightmost occurence of the number word
        # save it if it occurs after the previously found rightmost number
        pos_w_first = line.rfind(word)
        if pos_w_first > -1:
            pos_w_last = pos_w_first + len(word) - 1
            if pos_w_last > _pos:
                _pos = pos_w_last
                _digit = digit

        # find the rightmost occurence of the number digit
        # save it if it occurs after the previously found rightmost number
        pos_d = line.rfind(digit)
        if pos_d > -1:
            if pos_d > _pos:
                _pos = pos_d
                _digit = digit

    return _digit


answer_2 = 0
for line in lines:
    if line == "":
        continue
    left = find_left_digit(line)
    right = find_right_digit(line)
    number = int(left + right)
    answer_2 += number
print(answer_2)
