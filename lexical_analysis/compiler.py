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
rootNode = None
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
first_set = {
  'Program': [ 'Declaration', 'epsilon' ],
  'Declaration-list': [ 'Declaration', 'epsilon' ],
  'undefined': [ 'int', 'void' ],
  'Declaration-initial': [ 'int', 'void' ],
  'Declaration-prime': [ '(', ';', '[' ],
  'Var-declaration-prime': [ ';', '[' ],
  'Fun-declaration-prime': [ '(' ],
  'Type-specifier': [ 'int', 'void' ],
  'Params': [ 'int', 'void' ],
  'Param-list': [ ',', 'epsilon' ],
  'Param': [ 'int', 'void' ],
  'Param-prime': [ '[', 'epsilon' ],
  'Compound-stmt': [ '{' ],
  'Statement-list': [
    'epsilon', '{',
    'break',   ';',
    'if',      'repeat',
    'return',  'ID',
    '(',       'NUM'
  ],
  'Statement': [
    '{',      'break',
    ';',      'if',
    'repeat', 'return',
    'ID',     '(',
    'NUM'
  ],
  'Expression-stmt': [ 'break', ';', 'ID', '(', 'NUM' ],
  'Selection-stmt': [ 'if' ],
  'Iteration-stmt': [ 'repeat' ],
  'Return-stmt': [ 'return' ],
  'Return-stmt-prime': [ ';', 'ID', '(', 'NUM' ],
  'Expression': [ 'ID', '(', 'NUM' ],
  'B': [ '=', '[', '(', 'epsilon' ],
  'H': [ '=', '*', 'epsilon' ],
  'Simple-expression-zegond': [ '(', 'NUM' ],
  'Simple-expression-prime': [ '(', 'epsilon' ],
  'C': [ 'epsilon', '<', '==' ],
  'Relop': [ '<', '==' ],
  'Additive-expression': [ '(', 'ID', 'NUM' ],
  'Additive-expression-prime': [ '(', 'epsilon' ],
  'Additive-expression-zegond': [ '(', 'NUM' ],
  'D': [ 'epsilon', '+', '-' ],
  'Addop': [ '+', '-' ],
  'Term': [ '(', 'ID', 'NUM' ],
  'Term-prime': [ '(', 'epsilon' ],
  'Term-zegond': [ '(', 'NUM' ],
  'G': [ '*', 'epsilon' ],
  'Factor': [ '(', 'ID', 'NUM' ],
  'Var-call-prime': [ '(', '[', 'epsilon' ],
  'Var-prime': [ '[', 'epsilon' ],
  'Factor-prime': [ '(', 'epsilon' ],
  'Factor-zegond': [ '(', 'NUM' ],
  'Args': [ 'epsilon', 'ID', '(', 'NUM' ],
  'Arg-list': [ 'ID', '(', 'NUM' ],
  'Arg-list-prime': [ ',', 'epsilon' ]
}
follow_set = {

    'Program': ['$'],

    'Declaration-list': ['$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],

    'Declaration': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],

    'Declaration-initial': ['(', ';', '[', ',', ')'],

    'Declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],

    'Var-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],

    'Fun-declaration-prime': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}'],

    'Type-specifier': ['ID'],

    'Params': [')'],

    'Param-list': [')'],

    'Param': [',', ')'],

    'Param-prime': [',', ')'],

    'Compound-stmt': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else',

                      'until'],

    'Statement-list': ['}'],

    'Statement': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],

    'Expression-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],

    'Selection-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],

    'Iteration-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],

    'Return-stmt': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],

    'Return-stmt-prime': ['{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],

    'Expression': [';', ')', ']', ','],

    'B': [';', ')', ']', ','],

    'H': [';', ')', ']', ','],

    'Simple-expression-zegond': [';', ')', ']', ','],

    'Simple-expression-prime': [';', ')', ']', ','],

    'C': [';', ')', ']', ','],

    'Relop': ['(', 'ID', 'NUM'],

    'Additive-expression': [';', ')', ']', ','],

    'Additive-expression-prime': ['<', '==', ';', ')', ']', ','],

    'Additive-expression-zegond': ['<', '==', ';', ')', ']', ','],

    'D': ['<', '==', ';', ')', ']', ','],

    'Addop': ['(', 'ID', 'NUM'],

    'Term': ['+', '-', ';', ')', '<', '==', ']', ','],

    'Term-prime': ['+', '-', '<', '==', ';', ')', ']', ','],

    'Term-zegond': ['+', '-', '<', '==', ';', ')', ']', ','],

    'G': ['+', '-', '<', '==', ';', ')', ']', ','],

    'Factor': ['*', '+', '-', ';', ')', '<', '==', ']', ','],

    'Var-call-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],

    'Var-prime': ['*', '+', '-', ';', ')', '<', '==', ']', ','],

    'Factor-prime': ['*', '+', '-', '<', '==', ';', ')', ']', ','],

    'Factor-zegond': ['*', '+', '-', '<', '==', ';', ')', ']', ','],

    'Args': [')'],

    'Arg-list': [')'],

    'Arg-list-prime': [')']

}

parse_table = {
    "Program": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Declaration-list": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Declaration": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Declaration-initial": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Declaration-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Var-declaration-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Fun-declaration-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Type-specifier": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Params": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Param-list": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Param": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Param-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Compound-stmt": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Statement-list": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Statement": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Expression-stmt": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Selection-stmt": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Iteration-stmt": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Return-stmt": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Return-stmt-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Expression": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "B": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "H": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Simple-expression-zegond": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Simple-expression-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "C": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Relop": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Additive-expression": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Additive-expression-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Additive-expression-zegond": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "D": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Addop": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Term": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Term-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Term-zegond": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "G": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Factor": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Var-call-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Var-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Factor-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Factor-zegond": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Args": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Arg-list": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    },
    "Arg-list-prime": {
        "ID": None, "NUM": None, "void": None, "int": None, "break": None, "if": None, "else": None, "repeat": None, "until": None, "return": None,
        ")": None, "(": None, ";": None, "[": None, "]": None, ",": None, "$": None
    }
}
syntax_error_list = []
parserState = []


def main():
    global input_file, lookahead
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Token_Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
    # constructParsingTable()
    program()  # parse starts
    # write_parse_tree()
    # write_syntax_error()
    input_file.close()


def constructParsingTable():
    for nonTerminal in parse_table:
        for RHS in grammar[nonTerminal]:
            for terminal in parse_table[nonTerminal]:
                if terminal in first_set[RHS] and RHS != ["EPSILON"]:
                    parse_table[nonTerminal][terminal].append(RHS)
            if "EPSILON" in first_set[RHS]:
                for t in follow_set[RHS]:
                    if not parse_table[nonTerminal][t]:
                        parse_table[nonTerminal][t].append(RHS)  # list of some rules
            for t in follow_set[RHS]:
                if not parse_table[nonTerminal][t]:
                    parse_table[nonTerminal][t].append("synch")


def first(string):
    first_set = set()

    inputs = string.split()
    if len(inputs) > 1:
        for i in range(0, len(inputs)):
            first_set.update(first(inputs[i]))
            if ('EPSILON' in first_set) and (i != len(inputs) - 1):
                first_set.remove("EPSILON")
            elif 'EPSILON' not in first_set:
                break
        return first_set
    else:
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


def isNonTerminal(nonTerminal):
    return nonTerminal in grammar.keys()


def match(terminal):
    global lookahead
    if (terminal is Token_Type and lookahead.type.value == terminal) or lookahead == terminal:  # ID NUM
        lookahead = get_next_token(input_file)
    else:
        Syntax_Error("Fun-declaration-prime", errorType=Syntax_Error_Type.MISSING)  # not matched with declaration-list


def checkError(currentState):
    global lookahead
    if lookahead.lexeme in follow_set[currentState] or lookahead.type.value in follow_set[currentState]:  # synch no epsilon
        Syntax_Error(currentState,  errorType=Syntax_Error_Type.MISSING)
        return False
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        return True


def program():
    global lookahead, rootNode
    lookahead = get_next_token(input_file)
    if lookahead.lexeme in first("Declaration-list"):  # Program -> Declaration-list
        declaration_list()
    elif checkError("Program"):
        program()


def declaration_list():
    global lookahead

    if lookahead.lexeme in first("Declaration Declaration-list"):  # Declaration-list -> Declaration Declaration-list
        declaration()
        declaration_list()
    elif lookahead.lexeme in follow_set["Declaration-list"]:  # Declaration-list -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        declaration_list()


def declaration():
    global lookahead
    if lookahead.lexeme in first("Declaration-initial Declaration-prime"):  # Declaration -> Declaration-initial Declaration-prime
        declaration_initial()
        declaration_prime()
    elif checkError("Declaration"):
        declaration()


def declaration_initial():
    global lookahead
    if lookahead.lexeme in first("Type-specifier"):  # Declaration-initial -> Type-specifier ID
        type_specifier()
        match(Token_Type.ID)
    elif checkError("Declaration-initial"):
        declaration_initial()


def type_specifier():
    global lookahead
    if lookahead.lexeme == "int":  # Type-specifier -> int
        match("int")
    elif lookahead.lexeme == "void":  # Type-specifier -> void
        match("void")
    elif checkError("Type-specifier"):
        type_specifier()


def declaration_prime():
    global lookahead
    if lookahead.lexeme in first("Fun-declaration-prime"):  # Declaration-prime -> Fun-declaration-prime
        fun_declaration_prime()
    elif lookahead.lexeme in first("Var-declaration-prime"):  # Declaration-prime -> Var_declaration_prime
        var_declaration_prime()
    elif checkError("Declaration-prime"):
        declaration_prime()


def fun_declaration_prime():
    global lookahead
    # Fun-declaration-prime -> ( Params ) Compound-stmt
    if lookahead.lexeme == "(":
        match("(")
        params()
        match(")")
        compound_stmt()
    elif checkError("Fun-declaration-prime"):
        fun_declaration_prime()


def params():
    global lookahead
    if lookahead.lexeme == "int":  # Params -> int ID Param-prime Param-list
        match("int")
        match(Token_Type.ID)
        param_prime()
        param_list()
    elif lookahead.lexeme == "void":  # Params -> void
        match("void")
    elif checkError("Params"):
        params()


def var_declaration_prime():
    global lookahead
    if lookahead.lexeme == ";":  # Var-declaration-prime -> ;
        match(";")
    elif lookahead.lexeme == "[":  # Var-declaration-prime -> [ NUM ] ;
        match("[")
        match(Token_Type.NUM)
        match("]")
        match(";")
    elif checkError("Var-declaration-prime"):
        var_declaration_prime()


def param_list():
    global lookahead
    if lookahead.lexeme == ",":  # Param-list -> , Param Param-list
        match(",")
        params()
        param_list()
    elif lookahead.lexeme in follow_set["Param-list"] or lookahead.type.value in follow_set["Param-list"]:  # Param-list -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        param_list()


def param_prime():
    global lookahead
    if lookahead.lexeme == "[":  # Param-prime -> [ ]
        match("[")
        match("]")
    elif lookahead.lexeme in follow_set["Param-prime"] or lookahead.type.value in follow_set["Param-prime"]:  # Param-prime -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        param_prime()


def compound_stmt():
    global lookahead
    if lookahead.lexeme == "{":  # Compound-stmt -> { Declaration-list Statement-list }
        match("{")
        declaration_list()
        statement_list()
        match("}")
    elif checkError("Compound-stmt"):
        compound_stmt()


def statement_list():
    global lookahead
    if lookahead.lexeme in first("Statement Statement-list") or lookahead.type.value in first("Statement Statement-list"):  # Statement-list -> Statement Statement-list
        statement()
        statement_list()
    elif lookahead.lexeme in follow_set["Statement-list"] or lookahead.type.value in follow_set["Statement-list"]:  # Statement-list -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)  # not matched with declaration-list
        lookahead = get_next_token(input_file)
        statement_list()


def expression_stmt():
    global lookahead
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression"):  # Expression-stmt -> Expression ;
        expression()
        match(";")
    elif lookahead.lexeme == "break":  # Expression-stmt -> break ;
        match("break")
        match(";")
    elif lookahead.lexeme == ";":  # Expression-stmt -> ;
        match(";")
    elif checkError("Expression-stmt"):
        expression_stmt()


def selection_stmt():
    global lookahead
    # Selection-stmt -> if ( Expression ) Statement else Statement
    if lookahead.lexeme == "if":
        match("if")
        match("(")
        expression()
        match(")")
        statement()
        match("else")
        statement()
    elif checkError("Selection-stmt"):
        selection_stmt()


def iteration_stmt():
    global lookahead
    # Iteration-stmt -> repeat Statement until ( Expression )
    if lookahead.lexeme == "repeat":
        match("repeat")
        statement()
        match("until")
        match("(")
        expression()
        match(")")
    elif checkError("Iteration-stmt"):
        iteration_stmt()


def return_stmt_prime():
    global lookahead
    # Return-stmt-prime -> ; | Expression ;
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression"):
        expression()
        match(";")
    elif lookahead.lexeme == ";":
        match(";")
    elif checkError("Return-stmt-prime"):
        return_stmt_prime()


def return_stmt():
    global lookahead
    # Return-stmt -> return Return-stmt-prime
    if lookahead.lexeme == "return":
        match("return")
        return_stmt_prime()
    elif checkError("Return-stmt"):
        return_stmt()


def statement():
    global lookahead
    if lookahead.lexeme in first("Expression-stmt") or lookahead.type.value in first("Expression-stmt"):  # Statement -> Expression_stmt
        expression_stmt()
    elif lookahead.lexeme in first("Compound-stmt") or lookahead.type.value in first("Compound-stmt"):  # Statement -> Compound_stmt
        compound_stmt()
    elif lookahead.lexeme in first("Selection-stmt") or lookahead.type.value in first("Selection-stmt"):  # Statement -> Selection_stmt
        selection_stmt()
    elif lookahead.lexeme in first("Iteration-stmt") or lookahead.type.value in first("Iteration-stmt"):  # Statement -> Iteration_stmt
        iteration_stmt()
    elif lookahead.lexeme in first("Return-stmt") or lookahead.type.value in first("Return-stmt"):  # Statement -> Return_stmt
        return_stmt()
    elif lookahead.lexeme in follow_set["Statement"] or lookahead.type.value in follow_set["Statement"]:
        Syntax_Error("Statement", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        statement()


def simple_expression_zegond():
    global lookahead
    # Simple-expression-zegond -> Additive-expression-zegond C
    if lookahead.lexeme in first("Additive-expression-zegond C") or lookahead.type.value in first("Additive-expression-zegond C"):
        additive_expression_zegond()
        c()
    elif lookahead.lexeme in follow_set["Simple-expression-zegond"] or lookahead.type.value in follow_set["Simple-expression-zegond"]:
        Syntax_Error("Simple-expression-zegond", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        simple_expression_zegond()


def additive_expression_zegond():
    global lookahead
    # Additive-expression-zegond -> Term-zegond D
    if lookahead.lexeme in first("Term-zegond D") or lookahead.type.value in first("Term-zegond D"):
        term_zegond()
        d()
    elif lookahead.lexeme in follow_set["Additive-expression-zegond"] or lookahead.type.value in follow_set["Additive-expression-zegond"]:
        Syntax_Error("Additive-expression-zegond", errorType=Syntax_Error_Type.MISSING)
        # no node
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        additive_expression_zegond()


def expression():
    global lookahead
    # Expression -> Simple-expression-zegond | ID B
    if lookahead.lexeme in first("Simple-expression-zegond") or lookahead.type.value in first("Simple-expression-zegond"):  # Expression -> Simple_expression_zegond
        simple_expression_zegond()
    elif lookahead.type.value == Token_Type.ID:
        match(Token_Type.ID)
        b()
    elif lookahead.lexeme in follow_set["Expression"] or lookahead.type.value in follow_set["Expression"]:
        Syntax_Error("Expression", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        expression()


def relop():
    global lookahead
    if lookahead.lexeme == "<":  # Relop -> <
        match("<")
    elif lookahead.lexeme == "==":  # Relop -> ==
        match("==")
    elif lookahead.lexeme in follow_set["Relop"] or lookahead.type.value in follow_set["Relop"]:
        Syntax_Error("Relop", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        relop()


def c():
    global lookahead
    # C -> Relop Additive-expression | EPSILON
    if lookahead.lexeme in first("Relop Additive-expression") or lookahead.type.value in first("Relop Additive-expression"):  # C -> Relop Additive-expression
        relop()
        additive-expression()
    elif lookahead.lexeme in follow_set["C"] or lookahead.type.value in follow_set["C"]:  # C -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        c()


def addop():
    global lookahead
    # Addop -> + | -
    if lookahead.lexeme == "+":
        match("+")
    elif lookahead.lexeme == "-":
        match("-")
    elif lookahead.lexeme in follow_set["Addop"] or lookahead.type.value in follow_set["Addop"]:
        Syntax_Error("Addop", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        addop()


def d():
    global lookahead
    # D -> Addop Term D | EPSILON
    if lookahead.lexeme in first("Addop Term D") or lookahead.type.value in first("Addop Term D"):  # D -> Addop Term D
        addop()
        term()
        d()
    elif lookahead.lexeme in follow_set["D"] or lookahead.type.value in follow_set["D"]:  # D -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        d()


def term():
    global lookahead
    # Term -> Factor G
    if lookahead.lexeme in first("Factor G") or lookahead.type.value in first("Factor G"):
        factor()
        g()
    elif lookahead.lexeme in follow_set["Term"] or lookahead.type.value in follow_set["Term"]:
        Syntax_Error("Term", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        term()


def g():
    global lookahead
    if lookahead.lexeme == "*":  # G -> * Factor G
        match("*")
        factor()
        g()
    elif lookahead.lexeme in follow_set["G"] or lookahead.type.value in follow_set["G"]:  # G -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        g()


def var_call_prime():
    global lookahead
    if lookahead.lexeme == "(":  # Var-call-prime -> ( Args )
        match("(")
        args()
        match(")")
    elif lookahead.lexeme in first("Var-prime") or lookahead.type.value in first("Var-prime"):  # Var-call-prime -> Var-prime
        var_prime()
    elif lookahead.lexeme in follow_set["Var-call-prime"] or lookahead.type.value in follow_set["Var-call-prime"]:
        Syntax_Error("Var-call-prime", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        var_call_prime()


def factor():
    global lookahead
    # Factor -> ( Expression ) | ID Var-call-prime | NUM
    if lookahead.lexeme == "(":  # Factor -> ( Expression )
        match("(")
        expression()
        match(")")
    elif lookahead.type.value == Token_Type.ID:  # Factor -> ID Var-call-prime
        match(Token_Type.ID)
        var_call_prime()
    elif lookahead.type.value is Token_Type.NUM:  # Factor -> NUM
        match(Token_Type.NUM)
    elif lookahead.lexeme in follow_set["Factor"] or lookahead.type.value in follow_set["Factor"]:
        Syntax_Error("Factor", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        factor()


def arg_list():
    global lookahead
    # Arg-list -> Expression Arg-list-prime
    if lookahead.lexeme in first("Expression Arg-list-prime") or lookahead.type.value in first("Expression Arg-list-prime"):
        expression()
        arg_list_prime()
    elif lookahead.lexeme in follow_set["Arg-list"] or lookahead.type.value in follow_set["Arg-list"]:
        Syntax_Error("Arg-list", errorType=Syntax_Error_Type.MISSING)
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        arg_list()


def args():
    global lookahead
    # Args -> Arg-list | EPSILON
    if lookahead.lexeme in first("Arg-list") or lookahead.type.value in first("Arg-list"):  # Args -> Arg-list
        arg_list()
    elif lookahead.lexeme in follow_set["Args"] or lookahead.type.value in follow_set["Args"]:  # Args -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        args()


def arg_list_prime():
    global lookahead
    if lookahead.lexeme == ",":  # Arg-list-prime -> , Expression Arg-list-prime
        match(",")
        expression()
        arg_list_prime()
    elif lookahead.lexeme in follow_set["Arg-list-prime"] or lookahead.type.value in follow_set["Arg-list-prime"]:  # Arg-list-prime -> EPSILON
        return
    else:
        Syntax_Error(errorType=Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        arg_list_prime()


class Syntax_Error_Type(Enum):
    MISSING = "missing"
    ILLEGAL = "illegal"
    UNEXPECTED_EOF = "Unexpected EOF"


class Token_Type(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"


class Syntax_Error:
    def __init__(self, lexeme, type=Token_Type.KEYWORD, errorType=Syntax_Error_Type.MISSING):
        if lexeme == "":
            self.text = " " + errorType.value + " " + type.value
        else:
            self.text = " " + errorType.value + " " + lexeme
        self.line = lookahead.line
        self.errorType = errorType
        # if parse_table[nonTerminal][lookahead] == "synch":
        #
        # else:
        syntax_error_list.append(self)

    def __str__(self):
        return "#" + str(self.line) + " : syntax error, " + str(self.errorType) + text


def write_syntax_error():
    file = open("syntax_errors.txt", "w")
    if len(syntax_error_list) != 0:
        for error in syntax_error_list:
            file.write(str(error))
    else:
        file.write("There is no syntax error.")
    file.close()


def write_parse_tree():
    file = open("parse_tree.txt", "w")
    for pre, fill, node in RenderTree(rootNode):
        file.write("%s%s" % (pre, node.name))
    file.close()


class ERROR_Type(Enum):
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"


class Token:
    def __init__(self, lexeme="", type=Token_Type.ID, line=0, needToAddToTokenList=True):
        self.lexeme = lexeme
        self.type = type
        self.line = line
        if (type == Token_Type.ID or type == Token_Type.KEYWORD) and lexeme not in symbol_table:
            symbol_table.append(lexeme)
        if needToAddToTokenList and self not in token_list:
            token_list.append(self)

    def __str__(self):
        return "(" + self.type.name + ", " + self.lexeme + ")"


class Lexical_Error:
    def __init__(self, lexeme="", error_type=ERROR_Type.INVALID_INPUT, line=0):
        self.lexeme = lexeme
        self.type = error_type
        self.line = line
        error_list.append(self)

    def __str__(self):
        return "(" + self.lexeme + ", " + self.type.value + ")"


def get_next_token(file):
    state = 0
    TokenType = None
    lexeme = ""
    global lineno, characterBuffer

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
            Lexical_Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
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
            TokenType = Token_Type.NUM
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
            Lexical_Error(lexeme, ERROR_Type.INVALID_NUMBER, lineno)
        elif state == 3:
            state = 100
            TokenType = Token_Type.NUM
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
            TokenType = Token_Type.SYMBOL
        # handling invalid char after "="
        elif state == 5 and not nextCharacter:
            state = 7
        elif state == 5 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122
                                 or nextCharacter in digits or nextCharacter in symbols) \
                and not (nextCharacter.isspace()) and nextCharacter != "*" and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Lexical_Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 5:
            state = 100
            TokenType = Token_Type.SYMBOL
            characterBuffer = nextCharacter
        elif state == 7:
            state = 100
            TokenType = Token_Type.SYMBOL
            # matching WHITESPACE using state 8 & 9 & 10
        elif state == 0 and nextCharacter.isspace():
            lexeme += nextCharacter
            state = 100
            if nextCharacter == '\n':
                lineno += 1
            TokenType = Token_Type.WHITESPACE
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
            Lexical_Error("/*" + lexeme[0:5] + "...", ERROR_Type.UNCLOSED_COMMENT, comment_start_line)
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
            TokenType = Token_Type.COMMENT
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
            Lexical_Error(lexeme, ERROR_Type.UNMATCHED_COMMENT, lineno)
        elif state == 14 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122
                                  or nextCharacter in digits or nextCharacter in symbols) \
                and not (nextCharacter.isspace()) and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Lexical_Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
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
            Lexical_Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 16 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(
                nextCharacter) <= 122 or nextCharacter in digits or nextCharacter in symbols) and not (
                nextCharacter.isspace()) and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Lexical_Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 16:
            state = 100
            characterBuffer = nextCharacter
            Lexical_Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)

    out_put = None    

    if TokenType != Token_Type.COMMENT and TokenType != Token_Type.WHITESPACE and TokenType is not None:
        out_put = Token(lexeme, TokenType, lineno)
    else :
        out_put = get_next_token(input_file)

    return out_put


def findType(token):
    if token in keywords:
        return Token_Type.KEYWORD
    else:
        return Token_Type.ID


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
