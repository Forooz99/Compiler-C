from enum import Enum

# Alireza Foroodniya 99105645, Foroozan Iraji 99105272
digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
symbols = {";", ":", "{", "}", "[", "]", "(", ")", "<", "*", "+", "-", ","}
keywords = {"if", "else", "void", "int", "repeat", "break", "return", "until"}
symbol_table = []
token_list = []


class Type(Enum):
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6


class Token:
    def __init__(self, lexeme="", type=Type.ID, line=0, needToAddToTokenList=True):
        self.lexeme = lexeme
        self.type = type
        self.line = line
        if (type == Type.ID or type == Type.KEYWORD) and lexeme not in symbol_table:
            symbol_table.append(lexeme)
        if needToAddToTokenList and self not in token_list:
            token_list.append(self)

    def __str__(self):
        return "(" + self.type.name + ", " + self.lexeme + ")"


def main():
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
    characterBuffer = input_file.read(1)
    while get_next_token(input_file, characterBuffer):
        get_next_token(input_file, characterBuffer)
    input_file.close()

    for s in symbol_table:
        print(s)

    createOutputs()


def createOutputs():
    write_input = None
    for i in range(1, len(symbol_table)):
        write_input += str(i) + ".\t" + symbol_table[i - 1] + "\n"
    writeToFile("symbol_table.txt", write_input)

    write_input = None
    lineno = 0
    for token in token_list:
        if lineno != token.line:
            write_input += str(token.line) + ".\t"
            if lineno != 0:
                write_input += "\n"
            lineno += 1
        write_input += str(token) + " "
    writeToFile("tokens.txt", write_input)
    writeToFile("lexical_errors.txt", "There is no lexical error.")


def get_next_token(file, characterBuffer):
    state = 0
    TokenType = None
    lexeme = ""
    lineno = 0


    if characterBuffer:
        nextCharacter = characterBuffer
        characterBuffer = None
    else:
        nextCharacter = file.read(1)

    if not nextCharacter:
        return 0

    while state != 100:
        # matching ID and Keywords Using State 1 & 2
        if state == 0 and (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122):
            state = 1
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 1 and (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122 or nextCharacter in digits):
            state = 1
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 1:
            state = 100
            characterBuffer = nextCharacter
            TokenType = findType(lexeme)
        # matching NUM's Using State 3 & 4
        elif state == 0 and nextCharacter in digits:
            state = 3
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 3 and nextCharacter in digits:
            state = 3
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 3:
            state = 100
            TokenType = Type.NUM
            characterBuffer = nextCharacter
        # matching SYMBOL using state 5 & 6 & 7
        elif state == 0 and nextCharacter in symbols:
            state = 7
            lexeme += nextCharacter
        elif state == 0 and nextCharacter == "=":
            state = 5
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 5 and nextCharacter == "=":
            state = 100
            lexeme += nextCharacter
            TokenType = Type.SYMBOL
        elif state == 5:
            state = 100
            TokenType = Type.SYMBOL
            characterBuffer = nextCharacter
        elif state == 7:
            state = 100
            TokenType = Type.SYMBOL
        # matching WHITESPACE using state 8 & 9 & 10
        elif state == 0 and nextCharacter.isspace():
            lexeme += nextCharacter
            state = 8
        elif state == 8:
            state = 100
            TokenType = Type.WHITESPACE
        # matching comments using states starting from 11
        elif state == 0 and nextCharacter == "/":
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 11
        elif state == 11 and nextCharacter == "*":
            nextCharacter = file.read(1)
            lexeme = ""
            state = 12
        elif state == 11 and nextCharacter != "*":
            characterBuffer = nextCharacter
            state = 7
        elif state == 12 and nextCharacter != "*":
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 12
        elif state == 12 and nextCharacter == "*":
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 13
        elif state == 13 and nextCharacter != "/":
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 12
        elif state == 13 and nextCharacter == "/":
            lexeme = lexeme.rstrip(lexeme[-1])
            TokenType = Type.COMMENT
            state = 100
        # this state was used when incorrect nextCharacter is given
        elif state == 0:
            state = 100

    if lexeme == "\n":
        lineno += 1
    if TokenType != Type.COMMENT and TokenType != Type.WHITESPACE:
        Token(lexeme, TokenType, lineno)

    return 1


def findType(token):
    if token in keywords:
        return Type.KEYWORD
    else:
        return Type.ID


def writeToFile(fileName, data):
    file = open(fileName, "w")
    file.write(data)
    file.close()


main()
