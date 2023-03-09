import re
from scanner import Type


def tokenizer(line, i):
    state = 0
    j = i
    TokenType = Type.COMMENT
    while state != 100:

        # matching ID and Keywords's Using State 1 & 2
        if state == 0 and re.search("[a-zA-Z]", line[j]):
            state = 1
            j += 1



        elif state == 1 and re.search("[a-zA-Z0-9]", line[j]):

            state = 1
            j += 1
            if j > len(line) - 1:
                state = 2
                j -= 1



        elif state == 1 or state == 2:

            state = 100
            TokenType = findType(line[i:j])


        # matching NUM's Using State 3 & 4

        elif state == 0 and re.search("[0-9]", line[j]):
            state = 3
            j += 1


        elif state == 3 and re.search("[0-9]", line[j]):
            state = 3
            j += 1
            if j > len(line) - 1:
                state = 4
                j -= 1

        elif state == 3 or state == 4:
            state = 100
            TokenType = Type.Type.NUM


        # matching SYMBOL using state 5 & 6 & 7
        elif state == 0 and re.search("[;:{}\[\]()]", line[j]):
            j += 1
            if j > len(line) - 1:
                j -= 1
            state = 7

        elif state == 0 and re.search("[=]", line[j]):
            state = 5
            j += 1
            if j > len(line) - 1:
                j -= 1
                state = 7

        elif state == 5 and re.search("[=]", line[j]):
            j += 1
            if j > len(line) - 1:
                j -= 1

            state = 7



        elif state == 7 or state == 5:
            state = 100
            TokenType = Type.SYMBOL


        # matching WHITESPACE using state 8 & 9 & 10

        elif state == 0 and re.search("\s", line[j]):
            j += 1
            if j > len(line) - 1:
                j -= 1
            state = 8

        elif state == 8:
            state = 100
            TokenType = Type.WHITESPACE



        # this state was used when incorrect input is given
        elif state == 0:
            state = 100
            j += 1

    if TokenType != Type.COMMENT:
        print("(" + TokenType.name + "," + line[i: j] + ")")

    return j


def findType(input):
    if input == "if" or input == "else" or input == "void" or input == "int" or input == "repeat" or input == "break" or input == "until" or input == "return":
        return Type.KEYWORD
    else:
        return Type.ID


