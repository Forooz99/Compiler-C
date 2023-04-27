from enum import Enum

# Alireza Foroodniya 99105645, Foroozan Iraji 99105272
digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
symbols = {";", ":", "{", "}", "[", "]", "(", ")", "<", "+", "-", ","}
keywords = {"break", "else", "if", "int", "repeat", "return", "until", "void"}
symbol_table = []
token_list = []
error_list = []
characterBuffer = None
lineno = 1
input_file = None
lookahead = None
grammar = {
    "Program": [["Declaration-list"]],
    "Declaration-list": [["Declaration", "Declaration-list"], ["EPSILON"]],
    "Declaration": [["Declaration-initial", "Declaration-prime"]],
    "Declaration-initial": [["Type-specifier", "ID"]],
    "Declaration-prime": [["Fun-declaration-prime"], ["Var-declaration-prime"]],
    "Var-declaration-prime": [[";"], ["[", "NUM", "]", ";"]],
    "Fun-declaration-prime": [["(", "Params", ")", "Compound-stmt"]],
    "Type-specifier": [["int"], ["void"]],
    "Params": [["int", "ID", "Param-prime", "Param-list"], ["void"]],
    "Param-list": [[",", "Param", "Param-list"], ["EPSILON"]],
    "Param": [["Declaration-initial", "Param-prime"]],
    "Param-prime": [["[", "]"], ["EPSILON"]],
    "Compound-stmt": [["{", "Declaration-list", "Statement-list", "}"]],
    "Statement-list": [["Statement", "Statement-list"], ["EPSILON"]],
    "Statement": [["Expression-stmt"], ["Compound-stmt"], ["Selection-stmt"], ["Iteration-stmt"], ["Return-stmt"]],
    "Expression-stmt": [["Expression", ";"], ["break", ";"], [";"]],
    "Selection-stmt": [["if", "(", "Expression", ")", "Statement", "else", "Statement"]],
    "Iteration-stmt": [["repeat", "Statement", "until", "(", "Expression", ")"]],
    "Return-stmt": [["return", "Return-stmt-prime"]],
    "Return-stmt-prime": [["Expression", ";"], [";"]],
    "Expression": [["Simple-expression-zegond"], ["ID", "B"]],
    "B": [["=", "Expression"], ["[", "Expression", "]", "H"], ["Simple-expression-prime"]],
    "H": [["=", "Expression"], ["G", "D", "C"]],
    "Simple-expression-zegond": [["Additive-expression-zegond", "C"]],
    "Simple-expression-prime": [["Additive-expression-prime", "C"]],
    "C": [["Relop", "Additive-expression"], ["EPSILON"]],
    "Relop": [["<"], ["=="]],
    "Additive-expression": [["Term", "D"]],
    "Additive-expression-prime": [["Term-prime", "D"]],
    "Additive-expression-zegond": [["Term-zegond", "D"]],
    "D": [["Addop", "Term", "D"], ["EPSILON"]],
    "Addop": [["+"], ["-"]],
    "Term": [["Factor", "G"]],
    "Term-prime": [["Factor-prime", "G"]],
    "Term-zegond": [["Factor-zegond", "G"]],
    "G": [["*", "Factor", "G"], ["EPSILON"]],
    "Factor": [["(", "Expression", ")"], ["ID", "Var-call-prime"], ["NUM"]],
    "Var-call-prime": [["(", "Args", ")"], ["Var-prime"]],
    "Var-prime": [["[", "Expression", "]"], ["EPSILON"]],
    "Factor-prime": [["(", "Args", ")"], ["EPSILON"]],
    "Factor-zegond": [["(", "Expression", ")"], ["NUM"]],
    "Args": [["Arg-list"], ["EPSILON"]],
    "Arg-list": [["Expression", "Arg-list-prime"]],
    "Arg-list-prime": [[",", "Expression", "Arg-list-prime"], ["EPSILON"]]
}


def match(type, terminal= ''):
    global lookahead, input_file
    if lookahead == terminal:
        lookahead = get_next_token(input_file)
    else:
        return "error"


def first(string):
    return


def follow(nonTerminal):
    return


def program():
    declaration_list()


def declaration_list():
    if lookahead in first(declaration):
        declaration()
        declaration_list()
    else:
        return


def declaration():
    declaration_initial()
    declaration_prime()


def declaration_initial():
    type_specifier()
    match(Type.ID)


def declaration_prime():
    if lookahead in first(fun_declaration_prime):
        fun_declaration_prime()
    elif lookahead in first(var_declaration_prime):
        var_declaration_prime()
    else:
        print("error")


def var_declaration_prime():
    if lookahead == ";":
        match(Type.SYMBOL, ';')
    elif lookahead == "[":
        match(Type.SYMBOL, '[')
        match(Type.NUM)
        match(Type.SYMBOL, ']')
        match(Type.SYMBOL, ';')
    else:
        print("error")


def fun_declaration_prime():
    match(Type.SYMBOL, "(")
    params()
    match(Type.SYMBOL, ")")
    compound_stmt()


def type_specifier():
    if lookahead is Type.NUM:
        match(Type.NUM)
    elif lookahead == "void":
        match(Type.KEYWORD, "void")
    else:
        print("error")


def params():
    if lookahead == "int":
        match(Type.KEYWORD, "int")
        match(Type.ID)
        param_prime()
        param_list()
    elif lookahead == "void":
        match(Type.KEYWORD, "void")
    else:
        print("error")


def param_list():
    if lookahead == ",":
        match(Type.SYMBOL, ",")
        param()
        param_list()
    else:
        return


def param():
    declaration_initial()
    param_prime()


def param_prime():
    if lookahead == "]":
        match(Type.SYMBOL, "]")
        match(Type.SYMBOL, "[")
    else:
        return


def compound_stmt():
    match(Type.SYMBOL, "{")
    declaration_list()
    statement_list()
    match(Type.SYMBOL, "}")


def statement_list():
    if lookahead in first(statement):
        statement()
        statement_list()
    else:
        return


def statement():
    if lookahead in first(expression_stmt):
        expression_stmt()
    elif lookahead in first(compound_stmt):
        compound_stmt()
    elif lookahead in first(selection_stmt):
        selection_stmt()
    elif lookahead in first(iteration_stmt):
        iteration_stmt()
    elif lookahead in first(return_stmt):
        return_stmt()
    else:
        print("error")


def expression_stmt():
    if lookahead in first(expression):
        expression()
        match(Type.SYMBOL, ";")
    elif lookahead == "break":
        match(Type.KEYWORD, "break")
        match(Type.SYMBOL, ";")
    elif lookahead == ";":
        match(Type.SYMBOL, ";")
    else:
        print("error")


def selection_stmt():
    match(Type.KEYWORD, "if")
    match(Type.SYMBOL, "(")
    expression()
    match(Type.SYMBOL, ")")
    statement()
    match(Type.KEYWORD, "else")
    statement()


def iteration_stmt():
    match(Type.KEYWORD, "repeat")
    statement()
    match(Type.KEYWORD, "until")
    match(Type.SYMBOL, "(")
    expression()
    match(Type.SYMBOL, ")")


def return_stmt():
    match(Type.KEYWORD, "return")
    return_stmt_prime()


def return_stmt_prime():
    if lookahead in first(expression):
        expression()
        match(Type.SYMBOL, ";")
    elif lookahead == ";":
        match(Type.SYMBOL, ";")
    else:
        print("error")


def expression():
    if lookahead in first(simple_expression_zegond):
        simple_expression_zegond()
    elif lookahead is Type.ID:
        match(Type.ID)
        b()
    else:
        print("error")


def b():
    if lookahead == "=":
        match(Type.SYMBOL, "=")
        expression()
    elif lookahead == "[":
        match(Type.SYMBOL, "[")
        expression()
        match(Type.SYMBOL, "]")
        h()
    elif lookahead in first(simple_expression_prime):
        simple_expression_prime()
    else:
        print("error")


def h():
    if lookahead == "=":
        match(Type.SYMBOL, "=")
        expression()
    elif lookahead in first(g):
        g()
        d()
        c()
    else:
        print("error")


def simple_expression_zegond():
    additive_expression_zegond()
    c()


def simple_expression_prime():
    additive_expression_prime()
    c()


def c():
    if lookahead in first(relop):
        relop()
        additive_expression()
    else:
        return


def relop():
    if lookahead == "<":
        match(Type.SYMBOL, "<")
    elif lookahead == "==":
        match(Type.SYMBOL, "==")
    else:
        print("error")


def additive_expression():
    term()
    d()


def additive_expression_prime():
    term_prime()
    d()


def additive_expression_zegond():
    term_zegond()
    d()


def d():
    if lookahead in first(addop):
        addop()
        term()
        d()
    else:
        return


def addop():
    if lookahead == "+":
        match(Type.SYMBOL, "+")
    elif lookahead == "-":
        match(Type.SYMBOL, "-")
    else:
        print("error")


def term():
    factor()
    g()


def term_prime():
    factor_prime()
    g()


def term_zegond():
    factor_zegond()
    g()


def g():
    if lookahead == "*":
        match(Type.SYMBOL, "*")
        factor()
        g()
    else:
        return


def factor():
    if lookahead == "(":
        match(Type.SYMBOL, "(")
        expression()
        match(Type.SYMBOL, ")")
    elif lookahead is Type.ID:
        match(Type.ID)
        var_call_prime()
    elif lookahead is Type.NUM:
        match(Type.NUM)
    else:
        print("error")


def var_call_prime():
    if lookahead == "(":
        match(Type.SYMBOL, "(")
        args()
        match(Type.SYMBOL, ")")
    elif lookahead in first(var_prime):
        var_prime()
    else:
        print("error")


def var_prime():
    if lookahead == "[":
        match(Type.SYMBOL, "[")
        expression()
        match(Type.SYMBOL, "]")
    else:
        return


def factor_prime():
    if lookahead == "(":
        match(Type.SYMBOL, "(")
        args()
        match(Type.SYMBOL, ")")
    else:
        return


def factor_zegond():
    if lookahead == "(":
        match(Type.SYMBOL, "(")
        expression()
        match(Type.SYMBOL, ")")
    elif lookahead is Type.NUM:
        match(Type.NUM)
    else:
        print("error")


def args():
    if lookahead in first(arg_list):
        arg_list()
    else:
        return


def arg_list():
    expression()
    arg_list_prime()


def arg_list_prime():
    if lookahead == ",":
        match(Type.SYMBOL, ",")
        expression()
        arg_list_prime()
    else:
        return


def isNonTerminal(symbol):
    return symbol in grammar.keys()


class Type(Enum):
    NUM = 1
    ID = 2
    KEYWORD = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6


class ERROR_Type(Enum):
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"


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


class Error:
    def __init__(self, lexeme="", error_type=ERROR_Type.INVALID_INPUT, line=0):
        self.lexeme = lexeme
        self.type = error_type
        self.line = line
        error_list.append(self)

    def __str__(self) -> str:
        return "(" + self.lexeme + ", " + self.type.value + ")"


def main():
    global lookahead, input_file
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
    lookahead = get_next_token(input_file)

    while get_next_token(input_file):
        get_next_token(input_file)

    input_file.close()

    initial_error_writer()
    file_writer(token_list, "tokens.txt")
    file_writer(error_list, "lexical_errors.txt")
    symbol_writer()


def initial_error_writer():
    file = open("lexical_errors.txt", "w")
    file.write("There is no lexical error.")
    file.close()


def file_writer(content, file_name):
    if content:
        file = open(file_name, "w")
        string = str(content[0].line) + ".\t" + str(content[0]) + " "
        for i in range(1, len(content)):
            if content[i].line == content[i - 1].line:
                string += str(content[i]) + " "
            else:
                string += "\n"
                file.write(string)
                string = str(content[i].line) + ".\t" + str(content[i]) + " "
        file.write(string)
        file.close()


def symbol_writer():
    file = open("symbol_table.txt", "w")
    i = 1
    for symbol in symbol_table:
        string = str(i) + ".\t" + symbol + "\n"
        file.write(string)
        i += 1
    file.close()


def get_next_token(file):
    state = 0
    TokenType = None
    lexeme = ""
    global lineno
    global characterBuffer

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
        elif state == 1 and not nextCharacter:
            state = 100
            TokenType = findType(lexeme)
        elif state == 1 and (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122
                             or nextCharacter in digits):
            state = 1
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            # matching ERROR inside IDs
        elif state == 1 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122
                                 or nextCharacter in digits or nextCharacter in symbols) \
                and not (nextCharacter.isspace()) and nextCharacter != "*" \
                and nextCharacter != "/" and nextCharacter != "=":
            state = 2
            lexeme += nextCharacter
        elif state == 2:
            state = 100
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        # rest of matching IDs    
        elif state == 1:
            state = 100
            characterBuffer = nextCharacter
            TokenType = findType(lexeme)
        # matching NUM's and NUM ERROR Using State 3 & 4
        elif state == 0 and nextCharacter in digits:
            state = 3
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 3 and not nextCharacter:
            state = 100
            TokenType = Type.NUM
            characterBuffer = nextCharacter
        elif state == 3 and nextCharacter in digits:
            state = 3
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        # matching NUM ERRORS
        elif state == 3 and not (nextCharacter in digits) and not nextCharacter.isspace() \
                and not (nextCharacter in symbols) and nextCharacter != "=" and nextCharacter != "*" \
                and nextCharacter != "/":
            state = 4
            lexeme += nextCharacter
        elif state == 4:
            state = 100
            Error(lexeme, ERROR_Type.INVALID_NUMBER, lineno)
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
        # handling invalid char after "="
        elif state == 5 and not nextCharacter:
            state = 7
        elif state == 5 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122
                                 or nextCharacter in digits or nextCharacter in symbols) \
                and not (nextCharacter.isspace()) and nextCharacter != "*" and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
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
            state = 100
            if nextCharacter == '\n':
                lineno += 1
            TokenType = Type.WHITESPACE
            # matching comments using states starting from 11
        elif state == 0 and nextCharacter == "/":
            comment_start_line = lineno
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 11
        elif state == 11 and nextCharacter == "*":
            nextCharacter = file.read(1)
            lexeme = ""
            state = 12
        elif state == 11 and nextCharacter != "*":
            state = 16
        elif state == 12 and nextCharacter == "":
            Error("/*" + lexeme[0:5] + "...", ERROR_Type.UNCLOSED_COMMENT, comment_start_line)
            return 0
        elif state == 12 and nextCharacter != "*":
            lexeme += nextCharacter
            if nextCharacter == '\n':
                lineno += 1
            nextCharacter = file.read(1)
            state = 12
        elif state == 12 and nextCharacter == "*":
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 13
        elif state == 13 and nextCharacter == "*":
            state = 13
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 13 and nextCharacter != "/":
            lexeme += nextCharacter
            if nextCharacter == '\n':
                lineno += 1
            nextCharacter = file.read(1)
            state = 12
        elif state == 13 and nextCharacter == "/":
            lexeme = lexeme.rstrip(lexeme[-1])
            TokenType = Type.COMMENT
            state = 100
        # detecting unmatched comments using states 14
        elif state == 0 and nextCharacter == "*":
            state = 14
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        elif state == 14 and not nextCharacter:
            state = 7
        elif state == 14 and nextCharacter == "/":
            state = 100
            lexeme += nextCharacter
            Error(lexeme, ERROR_Type.UNMATCHED_COMMENT, lineno)
        elif state == 14 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122
                                  or nextCharacter in digits or nextCharacter in symbols) \
                and not (nextCharacter.isspace()) and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 14 and nextCharacter != "/":
            state = 7
            characterBuffer = nextCharacter
        # this state was used when incorrect nextCharacter is encountered 
        # I read next char because in case of "/" it must be read
        elif state == 0:
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 15
        elif state == 15:
            state = 100
            characterBuffer = nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 16 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(
                nextCharacter) <= 122 or nextCharacter in digits or nextCharacter in symbols) and not (
                nextCharacter.isspace()) and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 16:
            state = 100
            characterBuffer = nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)

    if TokenType != Type.COMMENT and TokenType != Type.WHITESPACE and TokenType is not None:
        Token(lexeme, TokenType, lineno)

    return 1


def findType(token):
    if token in keywords:
        return Type.KEYWORD
    else:
        return Type.ID





main()
