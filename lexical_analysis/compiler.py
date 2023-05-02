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
    "Program": ["EPSILON", "int", "void"],
    "Declaration-list": ["EPSILON", "int", "void"],
    "Declaration Declaration-list": ["int", "void"],
    "Declaration": ["int", "void"],
    "Declaration-initial Declaration-prime": ["int", "void"],
    "Declaration-initial": ["int", "void"],
    "Type-specifier ID": ["int", "void"],
    "Declaration-prime": ["(", ";", "["],
    "Var-declaration-prime": [";", "["],
    "Fun-declaration-prime": ["("],
    "( Params ) Compound-stmt": ["("],
    "Type-specifier": ["int", "void"],
    "Params": ["int", "void"],
    "Param-list": [",", "EPSILON"],
    "Param": ["int", "void"],
    "Declaration-initial Param-prime": ["int", "void"],
    "Param-prime": ["[", "EPSILON"],
    "Compound-stmt": ["{"],
    "Statement-list": ["EPSILON", "break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Statement Statement-list": [["break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"]],
    "Statement": ["break", ";", "ID", "(", "NUM", "if", "return", "{", "repeat"],
    "Expression-stmt": ["break", ";", "ID", "(", "NUM"],
    "Expression ;": ["ID", "(", "NUM"],
    "Selection-stmt": ["if"],
    "Iteration-stmt": ["repeat"],
    "Return-stmt": ["return"],
    "Return-stmt-prime": [";", "ID", "(", "NUM"],
    "Expression": ["ID", "(", "NUM"],
    "B": ["=", "[", "(", "EPSILON"],
    "H": ["=", "*", "EPSILON"],
    "G D C": ["*", "+", "-", "EPSILON", "<", "=="],
    "Simple-expression-zegond": ["(", "NUM"],
    "Additive-expression-zegond C": ["(", "NUM"],
    "Simple-expression-prime": ["(", "EPSILON"],
    "Additive-expression-prime C": ["(", "EPSILON", "<", "=="],
    "C": ["EPSILON", "<", "=="],
    "Relop Additive-expression": ["<", "=="],
    "Relop": ["<", "=="],
    "Additive-expression": ["(", "ID", "NUM"],
    "Term D": ["(", "ID", "NUM"],
    "Additive-expression-prime": ["(", "EPSILON"],
    "Term-prime D": ["(", "EPSILON", "+", "-"],
    "Additive-expression-zegond": ["(", "NUM"],
    "Term-zegond D": ["(", "NUM"],
    "D": ["EPSILON", "+", "-"],
    "Addop Term D": ["+", "-"],
    "Addop": ["+", "-"],
    "Term": ["(", "ID", "NUM"],
    "Factor G": ["(", "ID", "NUM"],
    "Term-prime": ["(", "EPSILON"],
    "Factor-prime G": ["(", "EPSILON", "*"],
    "Term-zegond": ["(", "NUM"],
    "Factor-zegond G": ["(", "NUM"],
    "G": ["*", "EPSILON"],
    "Factor": ["(", "ID", "NUM"],
    "Var-call-prime": ["(", "[", "EPSILON"],
    "Var-prime": ["[", "EPSILON"],
    "Factor-prime": ["(", "EPSILON"],
    "Factor-zegond": ["(", "NUM"],
    "Args": ["ID", "(", "NUM", "EPSILON"],
    "Arg-list": ["ID", "(", "NUM"],
    "Expression Arg-list-prime": ["ID", "(", "NUM"],
    "Arg-list-prime": [",", "EPSILON"]
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


def main():
    global input_file, lookahead
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Token_Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
   # constructParsingTable()
    startParsing()
    #write_parse_tree()
    # write_syntax_error()
    input_file.close()


def chooseWithParseTable(currentState):
    if currentState in grammar.keys():  # non terminal on top of stack
        if parse_table[currentState][lookahead] == "synch":
            Syntax_Error()
        elif parse_table[currentState][lookahead] is not None:
            return
        else: # empty cell
            Syntax_Error()


def startParsing():
    global lookahead
    parserState = "Program"
    lookahead = get_next_token(input_file)

    while lookahead != "$":
        # Program -> Declaration-list
        if parserState == "Program" and lookahead in first_set["Declaration-list"]:
            program = Node("Program")

            parserState = "Declaration-list"
        # Declaration-list -> Declaration Declaration-list
        elif parserState == "Declaration-list" and lookahead in first_set["Declaration Declaration-list"]:
            Node("Declaration-list")
            parserState = "Declaration"
        # Declaration-list -> EPSILON
        elif parserState == "Declaration-list":
            continue
        # Declaration -> Declaration-initial Declaration-prime
        elif parserState == "Declaration" and lookahead in first_set["Declaration-initial"]:
            Node("Declaration")
            parserState = "Declaration-initial"
        # Declaration-initial -> Type-specifier ID
        elif parserState == "Declaration-initial" and lookahead in first_set["Type-specifier"]:
            Node("Declaration-initial")
            parserState = "Type-specifier"
        # Declaration-prime -> Fun-declaration-prime
        elif parserState == "Declaration-prime" and lookahead in first_set["Fun-declaration-prime"]:
            Node("Declaration-prime")
            parserState = "Fun-declaration-prime"
        # Declaration-prime -> Var-declaration-prime
        elif parserState == "Declaration-prime" and lookahead in first_set["Var-declaration-prime"]:
            Node("Declaration-prime")
            parserState = "Var-declaration-prime"
        # Var-declaration-prime -> ;
        elif parserState == "Var-declaration-prime" and lookahead == ";":
            Node("Var-declaration-prime")
            lookahead = get_next_token(input_file)
        # Var-declaration-prime -> [ NUM ] ;
        elif parserState == "Var-declaration-prime" and lookahead == "[":
            Node("Var-declaration-prime")
            lookahead = get_next_token(input_file)
        # Fun-declaration-prime -> ( Params ) Compound-stmt
        elif parserState == "Fun-declaration-prime" and lookahead == "(":
            Node("Fun-declaration-prime")
            lookahead = get_next_token(input_file)
        # Type-specifier -> int | void
        elif parserState == "Type-specifier":
            Node("Type-specifier")
            if lookahead == "int":  # Type-specifier -> int
                match(Token_Type.KEYWORD, "int")
            elif lookahead == "void":  # Type-specifier -> void
                match(Token_Type.KEYWORD, "void")
            else:
                return Syntax_Error()
            match(Token_Type.ID)
        # Params -> int ID Param-prime Param-list
        elif parserState == "Params" and lookahead == "int":
            Node("Params")
            lookahead = get_next_token(input_file)
        # Params -> void
        elif parserState == "Params" and lookahead == "void":
            Node("Params")
            lookahead = get_next_token(input_file)
        # Param-list -> , Param Param-list
        elif parserState == "Param-list" and lookahead == ",":
            Node("Param-list")
            lookahead = get_next_token(input_file)
        # Param-list -> EPSILON
        elif parserState == "Fun_declaration_prime":
            Node("Declaration-list")
            continue
        # Param -> Declaration-initial Param-prime
        elif parserState == "Param" and lookahead in first_set["Declaration-initial Param-prime"]:
            Node("Param")
            parserState = "Declaration-initial"
        # Param-prime -> [ ]
        elif parserState == "Param-prime" and lookahead == "[":
            Node("Param-prime")
            lookahead = get_next_token(input_file)
        # Param-prime -> EPSILON
        elif parserState == "Param-prime":
            continue
        # Compound-stmt -> { Declaration-list Statement-list }
        elif parserState == "Compound-stmt" and lookahead == "{":
            Node("Compound-stmt")
            lookahead = get_next_token(input_file)
        # Statement-list -> Statement Statement-list
        elif parserState == "Statement-list" and lookahead in first_set["Statement Statement-list"]:
            Node("Statement-list")
            parserState = "Statement"
        # Statement-list -> EPSILON
        elif parserState == "Statement-list":
            continue
        # Statement -> Expression-stmt
        elif parserState == "Statement" and lookahead in first_set["Expression-stmt"]:
            Node("Statement")
            parserState = "Expression-stmt"
        # Statement -> Compound-stmt
        elif parserState == "Statement" and lookahead in first_set["Compound-stmt"]:
            Node("Statement")
            parserState = "Compound-stmt"
        # Statement -> Selection-stmt
        elif parserState == "Statement" and lookahead in first_set["Selection-stmt"]:
            Node("Statement")
            parserState = "Selection-stmt"
        # Statement -> Iteration-stmt
        elif parserState == "Statement" and lookahead in first_set["Iteration-stmt"]:
            Node("Statement")
            parserState = "Iteration-stmt"
        # Statement -> Return-stmt
        elif parserState == "Statement" and lookahead in first_set["Return-stmt"]:
            Node("Statement")
            parserState = "Return-stmt"
        # Expression-stmt -> Expression ;
        elif parserState == "Expression-stmt" and lookahead in first_set["Expression"]:
            Node("Expression-stmt")
            parserState = "Expression"
        # Expression-stmt -> break ;
        elif parserState == "Expression-stmt" and lookahead == "break":
            Node("Expression-stmt")
            lookahead = get_next_token(input_file)
        # Expression-stmt -> ;
        elif parserState == "Expression-stmt" and lookahead == ";":
            Node("Expression-stmt")
            lookahead = get_next_token(input_file)
        # Selection-stmt -> if ( Expression ) Statement else Statement
        elif parserState == "Selection-stmt" and lookahead == "if":
            Node("Selection-stmt")
            lookahead = get_next_token(input_file)
        # Iteration-stmt -> repeat Statement until ( Expression )
        elif parserState == "Iteration-stmt" and lookahead == "repeat":
            Node("Iteration-stmt")
            lookahead = get_next_token(input_file)
        # Return-stmt -> return Return-stmt-prime
        elif parserState == "Return-stmt" and lookahead == "return":
            Node("Return-stmt")
            lookahead = get_next_token(input_file)
        # Return-stmt-prime -> ;
        elif parserState == "Return-stmt-prime" and lookahead == ";":
            Node("Return-stmt-prime")
            lookahead = get_next_token(input_file)
        # Return-stmt-prime -> Expression ;
        elif parserState == "Return-stmt-prime" and lookahead in first_set["Expression"]:
            Node("Return-stmt-prime")
            parserState = "Expression"
        # Expression -> Simple-expression-zegond
        elif parserState == "Expression" and lookahead in first_set["Simple-expression-zegond"]:
            Node("Expression")
            parserState = "Simple-expression-zegond"
        # Expression -> ID B
        elif parserState == "Expression" and lookahead == "ID":
            Node("Expression")
            lookahead = get_next_token(input_file)

        # B -> = Expression
        elif parserState == "B" and lookahead == "=":
            Node("B")
            lookahead = get_next_token(input_file)

        # B -> [ Expression ] H
        elif parserState == "B" and lookahead == "[":
            Node("B")
            lookahead = get_next_token(input_file)
        # B -> Simple-expression-prime
        elif parserState == "B" and lookahead in first_set["Simple-expression-prime"]:
            Node("B")
            parserState = "Simple-expression-prime"
        # H -> = Expression
        elif parserState == "H" and lookahead == "=":
            Node("H")
            lookahead = get_next_token(input_file)
        # H -> G D C
        elif parserState == "H" and lookahead in first_set["G"]:
            Node("H")
            parserState = "G"

        # Simple-expression-zegond -> Additive-expression-zegond C
        elif parserState == "Simple-expression-zegond" and lookahead in first_set["Additive-expression-zegond C"]:
            Node("Simple-expression-zegond")
            parserState = "Additive-expression-zegond"

        # Simple-expression-prime -> Additive-expression-prime C
        elif parserState == "Simple-expression-prime" and lookahead in first_set["Additive-expression-prime C"]:
            Node("Simple-expression-prime")
            parserState = "Additive-expression-prime"

        # C -> Relop Additive-expression
        elif parserState == "C" and lookahead in first_set["Relop Additive-expression"]:
            Node("C")
            parserState = "Relop"

        # C -> EPSILON
        elif parserState == "C":
            continue

        # Relop -> <
        elif parserState == "Relop" and lookahead == "<":
            Node("Relop")
            lookahead = get_next_token(input_file)
        # Relop -> ==
        elif parserState == "Relop" and lookahead == "==":
            Node("Relop")
            lookahead = get_next_token(input_file)
        # Additive-expression -> Term D
        elif parserState == "Additive-expression" and lookahead in first_set["Term D"]:
            Node("Additive-expression")
            parserState = "Term"
        # Additive-expression-prime -> Term-prime D
        elif parserState == "Additive-expression-prime" and lookahead in first_set["Term-prime D"]:
            Node("Additive-expression-prime")
            parserState = "Term-prime"

        # Additive-expression-zegond -> Term-zegond D
        elif parserState == "Additive-expression-zegond" and lookahead in first_set["Term-zegond D"]:
            Node("Additive-expression-zegond")
            parserState = "Term-zegond"
        # D -> Addop Term D
        elif parserState == "D" and lookahead in first_set["Addop Term D"]:
            Node("D")
            parserState = "Addop"
        # D -> EPSILON
        elif parserState == "D":
            continue
        # Addop -> + | -
        elif parserState == "Addop" and lookahead == "+":
            Node("Addop")
            lookahead = get_next_token(input_file)
        # Addop -> + | -
        elif parserState == "Addop" and lookahead == "-":
            Node("Addop")
            lookahead = get_next_token(input_file)
        # Term -> Factor G
        elif parserState == "Term" and lookahead in first_set["Factor G"]:
            Node("Term")
            parserState = "Factor"
        # Term-prime -> Factor-prime G
        elif parserState == "Term-prime" and lookahead in first_set["Factor-prime G"]:
            Node("Term-prime")
            parserState = "Factor-prime"
        # Term-zegond -> Factor-zegond G
        elif parserState == "Term-zegond" and lookahead in first_set["Factor-zegond G"]:
            Node("Term-zegond")
            parserState = "Factor-zegond"

        # G -> * Factor G
        elif parserState == "G" and lookahead == "*":
            Node("G")
            lookahead = get_next_token(input_file)
        # G -> EPSILON
        elif parserState == "G":
            continue
        # Factor -> ( Expression )
        elif parserState == "Factor" and lookahead == "(":
            Node("Factor")
            lookahead = get_next_token(input_file)
        # Factor -> ID Var-call-prime
        elif parserState == "Factor" and lookahead == "ID":
            Node("Factor")
            lookahead = get_next_token(input_file)
        # Factor -> NUM
        elif parserState == "Factor" and lookahead == "NUM":
            Node("Factor")
            lookahead = get_next_token(input_file)
        # Var-call-prime -> ( Args )
        elif parserState == "Var-call-prime" and lookahead == "(":
            Node("Var-call-prime")
            lookahead = get_next_token(input_file)
        # Var-call-prime -> Var-prime
        elif parserState == "Var-call-prime" and lookahead == "Var-prime":
            Node("Var-call-prime")
            parserState = "Var-prime"
        # Var-prime -> [ Expression ]
        elif parserState == "Var-prime" and lookahead == "[":
            Node("Var-prime")
            lookahead = get_next_token(input_file)
        # Var-prime -> EPSILON
        elif parserState == "Var-prime":
            continue
        # Factor-prime -> ( Args )
        elif parserState == "Factor-prime" and lookahead == "(":
            Node("Factor-prime")
            lookahead = get_next_token(input_file)
        # Factor-prime -> EPSILON
        elif parserState == "Factor-prime":
            continue
        # Factor-zegond -> ( Expression )
        elif parserState == "Factor-zegond" and lookahead == "(":
            Node("Factor-zegond")
            lookahead = get_next_token(input_file)
        # Factor-zegond -> NUM
        elif parserState == "Factor-zegond" and lookahead == "NUM":
            Node("Factor-zegond")
            lookahead = get_next_token(input_file)
        # Args -> Arg-list
        elif parserState == "Args" and lookahead in first_set["Arg-list"]:
            Node("Args")
            parserState = "Arg-list"
        # Args -> EPSILON
        elif parserState == "Args":
            continue
        # Arg-list -> Expression Arg-list-prime
        elif parserState == "Arg-list" and lookahead in first_set["Expression Arg-list-prime"]:
            Node("Arg-list")
            parserState = "Expression"
        # Arg-list-prime -> , Expression Arg-list-prime
        elif parserState == "Arg-list-prime" and lookahead == ",":
            Node("Arg-list-prime")
            lookahead = get_next_token(input_file)
        # Arg-list-prime -> EPSILON
        elif parserState == "Arg-list-prime":
            continue


def constructParsingTable():
    for nonTerminal in parse_table:  # non-Terminal as key, first index
        for RHS in grammar[nonTerminal]:
            formatRule = formatProduction(RHS)
            for terminal in parse_table[nonTerminal]:  # terminal as second index
                if terminal in first_set[formatRule] and formatRule != ['EPSILON']:
                    parse_table[nonTerminal][terminal] = formatRule
            if "EPSILON" in first_set[formatRule]:
                for t in follow_set[formatRule.split(" ")[0]]:
                    parse_table[nonTerminal][t] = formatRule
                if "$" in follow_set[formatRule.split(" ")[0]]:
                    parse_table[nonTerminal]["$"] = formatRule
            for t in follow_set[formatRule.split(" ")[0]]:
                if parse_table[nonTerminal][t] is not None:
                    parse_table[nonTerminal][t] = "synch"


def formatProduction(rule_list):
    concatRule = ""
    for i in range(len(rule_list)):
        if i == len(rule_list) - 1:
            concatRule += rule_list[i]
            return concatRule
        else:
            concatRule += rule_list[i] + " "


class Syntax_Error_Type(Enum):
    MISSING = "missing"
    ILLEGAL = "illegal"
    UNEXPECTED_EOF = "Unexpected EOF"


class Syntax_Error:
    def __init__(self, token, errorType=Syntax_Error_Type.MISSING):
        self.line = token.line
        self.errorType = errorType
        if token.type == Token_Type.SYMBOL or token.type == Token_Type.KEYWORD:
            self.text = token.lexeme
        else:
            self.text = token.type
        syntax_error_list.append(self)

    def __str__(self):
        return "#" + str(self.line) + " : syntax error, " + str(self.errorType) + " " + text  # ????????


def write_parse_tree():
    global rootNode
    file = open("parse_tree.txt", "w")
    for pre, fill, node in RenderTree(rootNode):
        file.write("%s%s" % (pre, node.name))
    file.close()


def write_syntax_error():
    file = open("syntax_errors.txt", "w")
    if len(syntax_error_list) != 0:
        for error in syntax_error_list:
            file.write(str(error))
    else:
        file.write("There is no syntax error.")
    file.close()


class Token_Type(Enum):
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
