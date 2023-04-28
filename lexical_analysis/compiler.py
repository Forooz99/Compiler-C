from enum import Enum
from anytree import Node, RenderTree

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
token_stack = ['$']
rule_stack = ['$']
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
parse_table = {
    "Program": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Declaration-list": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Declaration": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Declaration-initial": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Declaration-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Var-declaration-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Fun-declaration-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Type-specifier": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Params": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Param-list": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Param": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Param-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Compound-stmt": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Statement-list": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Statement": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Expression-stmt": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Selection-stmt": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Iteration-stmt": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Return-stmt": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Return-stmt-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Expression": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "B": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "H": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Simple-expression-zegond": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Simple-expression-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "C": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Relop": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Additive-expression": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Additive-expression-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Additive-expression-zegond": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "D": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Addop": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Term": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Term-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Term-zegond": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "G": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Factor": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Var-call-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Var-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Factor-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Factor-zegond": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Args": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Arg-list": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    },
    "Arg-list-prime": {
        "ID": [], "NUM": [], "void": [], "int": [], "break": [], "if": [], "else": [], "repeat": [], "until": [], "return": [],
        ")": [], "(": [], ";": [], "[": [], "]": [], ",": [], "$": []
    }
}
syntax_error_list = []

first_set = {
    "Program": ["EPSILON", "int", "void"],
    "Declaration-list": ["EPSILON", "int", "void"],
    "Declaration": ["int", "void"],
    "Declaration-initial": ["int", "void"],
    "Declaration-prime": ["(", ";", "["],
    "Var-declaration-prime": [";", "["],
    "Fun-declaration-prime": ["("],
    "Type-specifier": ["int", "void"],
    "Params": ["int", "void"],
    "Param-list": [",", "EPSILON"],
    "Param": ["int", "void"],
    "Param-prime": ["[", "EPSILON"],
    "Compound-stmt": ["{"],
    "Statement-list": ["EPSILON", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Statement": ["break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Expression-stmt": ["break", ";", "ID", "(", "NUM"],
    "Selection-stmt": ["if"],
    "Iteration-stmt": ["repeat"],
    "Return-stmt": ["return"],
    "Return-stmt-prime": [";", "ID", "(", "NUM"],
    "Expression": ["ID", "(", "NUM"],
    "B": ["=", "[", "(", "EPSILON"],
    "H": ["=", "*", "EPSILON"],
    "Simple-expression-zegond": ["(", "NUM"],
    "Simple-expression-prime": ["(", "EPSILON"],
    "C": ["EPSILON", "<", "=="],
    "Relop": [["<"], ["=="]],
    "Additive-expression": ["(", "ID", "NUM"],
    "Additive-expression-prime": ["(", "EPSILON"],
    "Additive-expression-zegond": ["(", "NUM"],
    "D": ["EPSILON", "+", "-"],
    "Addop": ["+", "-"],
    "Term": ["(", "ID", "NUM"],
    "Term-prime": ["(", "EPSILON"],
    "Term-zegond": ["(", "NUM"],
    "G": ["*", "EPSILON"],
    "Factor": ["(", "ID", "NUM"],
    "Var-call-prime": ["(", "[", "EPSILON"],
    "Var-prime": ["[", "EPSILON"],
    "Factor-prime": ["(", "EPSILON"],
    "Factor-zegond": ["(", "NUM"],
    "Args": ["ID", "(", "NUM", "EPSILON"],
    "Arg-list": ["ID", "(", "NUM"],
    "Arg-list-prime": [",", "EPSILON"],
    ";": [";"], ",": [","], "]": ["]"], "[": ["["], ")": [")"], "(": ["("], "}": ["}"], "{": ["{"],
    "=": ["="], "==": ["=="], "<": ["<"], "+": ["+"], "-": ["-"], "*": ["*"],
    "ID": ["ID"], "NUM": ["NUM"], "int": ["int"], "void": ["void"], "break": ["break"], "if": ["if"], "else": ["else"],
    "repeat": ["repeat"], "until": ["until"], "return": ["return"], "EPSILON": ["EPSILON"]
}


follow_set = {
    "Program": ["$"],
    "Declaration-list": ["break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat", "$"],
    "Declaration": ["int", "void"],
    "Declaration-initial": ["[", "(", ";"],
    "Declaration-prime": ["int", "void"],
    "Var-declaration-prime": ["int", "void"],
    "Fun-declaration-prime": ["int", "void"],
    "Type-specifier": ["ID"],
    "Params": [")"],
    "Param-list": [")"],
    "Param": [","],
    "Param-prime": [","],
    "Compound-stmt": ["until", "else", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat", "int", "void"],
    "Statement-list": ["}"],
    "Statement": ["until", "else", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Expression-stmt": ["until", "else", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Selection-stmt": ["until", "else", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Iteration-stmt": ["until", "else", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Return-stmt": ["until", "else", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Return-stmt-prime": ["until", "else", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Expression": [",", ")", "]", ";"],
    "B": [",", ")", "]", ";"],
    "H": [",", ")", "]", ";"],
    "Simple-expression-zegond": [",", ")", "]", ";"],
    "Simple-expression-prime": [",", ")", "]", ";"],
    "C": [",", ")", "]", ";"],
    "Relop": ["(", "ID", "NUM"],
    "Additive-expression": [",", ")", "]", ";"],
    "Additive-expression-prime": ["<", "=="],
    "Additive-expression-zegond": ["<", "=="],
    "D": ["<", "==", ",", ")", "]", ";"],
    "Addop": ["(", "ID", "NUM"],
    "Term": ["+", "-"],
    "Term-prime": ["+", "-"],
    "Term-zegond": ["+", "-"],
    "G": ["+", "-"],
    "Factor": ["*"],
    "Var-call-prime": ["*"],
    "Var-prime": ["*"],
    "Factor-prime": ["*"],
    "Factor-zegond": ["*"],
    "Args": [")"],
    "Arg-list": [")"],
    "Arg-list-prime": [")"]
}


def startParsing():
    global lookahead
    constructParsingTable()
    initial_syntax_error_writer()

    # for nonTerminal in parse_table:
    #     print("")
    #     print(nonTerminal, end="        ")
    #     for terminal in parse_table["Program"].keys():
    #         print(str(parse_table[nonTerminal][terminal]) + ", " + str(terminal), end="    ")

    rule_stack.append("Program")  # push start state
    lookahead = get_next_token(input_file)
    while rule_stack:
        if lookahead == "$":
            print("parse end")
            break
        currentRule = rule_stack[-1]
        if currentRule == "EPSILON":
            rule_stack.pop()  # if state = epsilon pop and go to see state on top of stack
            continue
        if not isNonTerminal(currentRule) or currentRule == "$":  # terminal state & on top of stack
            if currentRule == lookahead:
                rule_stack.pop()
                lookahead = get_next_token(input_file)
                # create leaf node
            else:
                rule_stack.pop()
        else:  # non terminal state on top of stack

            if not parse_table[currentRule][lookahead]:  # have transition
                rule_stack.pop()
                # create interior node
                rule_stack.append(parse_table[currentRule][lookahead])
            elif parse_table[currentRule][lookahead] == "synch":
                rule_stack.pop()
            else:  # empty cell
                lookahead = get_next_token(input_file)


def initial_syntax_error_writer():
    file = open("syntax_errors.txt", "w")
    file.write("There is no syntax error.")
    file.close()


def constructParsingTable():
    for nonTerminal in parse_table:
        firstSet = first(nonTerminal)
        followSet = follow(nonTerminal)
        for RHS in grammar[nonTerminal]:
            for terminal in parse_table[nonTerminal]:
                if terminal in firstSet and RHS != ['EPSILON']:
                    parse_table[nonTerminal][terminal].append(RHS)
            if "EPSILON" in firstSet:
                for t in followSet:
                    if not parse_table[nonTerminal][t]:
                        parse_table[nonTerminal][t].append(RHS)   # list of some rules
            for t in followSet:
                if not parse_table[nonTerminal][t]:
                    parse_table[nonTerminal][t].append("synch")


def first(string):
    first_set = set() 
    
    terminal_has_epsilon = False
    if isNonTerminal(string):
        for rule in grammar[string]:
            new_rule = True
            rule_has_epsilon = False
            go_next = False
            for item in rule:
                

                if new_rule:
                    new_rule = False
                    first_set = first_set | first(item)
                    if "EPSILON" in first_set:
                        go_next = True
                        first_set.remove("EPSILON")
                        rule_has_epsilon = True
                        

                elif "EPSILON" in first_set or go_next:
                    go_next = False
                    if "EPSILON" in first_set:
                        first_set.remove("EPSILON")
                    first_set = first_set | first(item)
                    rule_has_epsilon = rule_has_epsilon and ("EPSILON" in first_set)

            if "EPSILON" in first_set:
                first_set.remove("EPSILON")
            terminal_has_epsilon = terminal_has_epsilon or rule_has_epsilon

    else:
        first_set.add(string)  # first(terminal) = terminal

    if terminal_has_epsilon:
        first_set.add("EPSILON")

    return first_set


def follow(nonTerminal):
    follow_set = set()
    return follow_set


def isNonTerminal(symbol):
    return symbol in grammar.keys()


def main():
    global input_file
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
    startParsing()
    input_file.close()


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
        return "$"

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


main()
