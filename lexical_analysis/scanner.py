from enum import Enum
import tokenizer
# Alireza Foroodniya 99105645, Foroozan Iraji 99105272

# token type: NUM / ID / KEYWORD / SYMBOL / COMMENT / WHITESPACE
# list for each type except comment, whitespace(these will be ignored):
num_list = []
id_list = []
keyword_list = []
symbol_list = []
symbol_table = []


class Type(Enum):
    KEYWORD = 1
    ID = 2
    NUM = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6


class Token:
    def __init__(self, lexeme="", type=Type.ID, tokenList=None, needToAdd=False):
        if tokenList is None:
            tokenList = id_list
        self.lexeme = lexeme
        self.type = type
        tokenList.append(lexeme)
        if needToAdd and self not in symbol_table:
            symbol_table.append(self)


# KEYWORD:  if/else/void/int/repeat/break/until/return
if_Keyword = Token("if", Type.KEYWORD, keyword_list)
else_Keyword = Token("else", Type.KEYWORD, keyword_list)
void_Keyword = Token("void", Type.KEYWORD, keyword_list)
int_Keyword = Token("int", Type.KEYWORD, keyword_list)
repeat_keyword = Token("repeat", Type.KEYWORD, keyword_list)
break_Keyword = Token("break", Type.KEYWORD, keyword_list)
until_keyword = Token("until", Type.KEYWORD, keyword_list)
return_keyword = Token("return", Type.KEYWORD, keyword_list)

# SYMBOL:   ; : , [ ] ( ) { } + - * = < ==
semicolon = Token(";", Type.SYMBOL, symbol_list)
colon = Token(":", Type.SYMBOL, symbol_list)
comma = Token(",", Type.SYMBOL, symbol_list)
openBracket = Token("[", Type.SYMBOL, symbol_list)
closeBracket = Token("]", Type.SYMBOL, symbol_list)
openParentheses = Token("(", Type.SYMBOL, symbol_list)
closeParentheses = Token(")", Type.SYMBOL, symbol_list)
openCurlyBraces = Token("{", Type.SYMBOL, symbol_list)
closeCurlyBraces = Token("}", Type.SYMBOL, symbol_list)
plus = Token("+", Type.SYMBOL, symbol_list)
minus = Token("-", Type.SYMBOL, symbol_list)
star = Token("*", Type.SYMBOL, symbol_list)
equal = Token("=", Type.SYMBOL, symbol_list)
lessThan = Token("<", Type.SYMBOL, symbol_list)
doubleEqual = Token("==", Type.SYMBOL, symbol_list)

token_list = []


def get_next_token(line):
    lexemeBeginning = 0
    forwardPointer = 0

    id_regex = "[a-zA-Z][a-zA-Z0-9]*"
    num_regex = "[0-9]+"
    whiteSpace_regex = "\s"

    while forwardPointer < len(line):
        forwardPointer += 1
        string = line[lexemeBeginning:forwardPointer]
        print(string)
        if matchSymbol(string) is Token:
            lexemeBeginning = forwardPointer + 1
            continue
        if matchIDAndKeyword(string) is Token:
            lexemeBeginning = forwardPointer + 1
            continue

        if matchNum(string) is Token:
            lexemeBeginning = forwardPointer + 1



    # return (token type,token string)
    # priority: symbol, keyword, id, num

def matchIDAndKeyword(string):
    return string


def matchSymbol(string):
    if string in symbol_list:
        return Token(string, Type.SYMBOL, symbol_list, True)
    return string


def matchKeyword(string):
    if string in keyword_list:
        return Token(string, Type.KEYWORD, keyword_list, True)
    return string


def matchNum(string):
    return string


def matchID(string):
    if string in id_list:
        return Token(string, Type.ID, id_list, True)
    return string


def main():
    lineNo = 0
    input_file = open("input.txt", "r")
    i = 0
    while True:
        line = input_file.readline().rstrip()
        if not line:
            break
        lineNo += 1
        while i != len(line) - 1:
            i = tokenizer.tokenizer(line, i)

        i = 0
    input_file.close()


main()
