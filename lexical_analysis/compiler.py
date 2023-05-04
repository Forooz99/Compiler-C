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
first__set = {}
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
    'Compound-stmt': ['int', 'void', '$', '{', 'break', ';', 'if', 'repeat', 'return', 'ID', '(', 'NUM', '}', 'else', 'until'],
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
syntax_error_list = []


def main():
    global input_file
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Token_Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
    program()  # parse starts
#    write_parse_tree()
    write_syntax_error()
    input_file.close()


def first(string):
    first_set = set()

    if string in first__set.keys():
        return first__set[string] 

    inputs = string.split()
    if len(inputs) > 1:
        for i in range(0, len(inputs)):
            first_set.update(first(inputs[i]))
            if ('EPSILON' in first_set) and (i != len(inputs) - 1):
                first_set.remove("EPSILON")
            elif 'EPSILON' not in first_set:
                break
        first__set[string] = first_set    
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
        first__set[string] = first_set 
        return first_set


def isNonTerminal(nonTerminal):
    return nonTerminal in grammar.keys()


def match(terminal):
    global lookahead
    if (((terminal == Token_Type.ID) or (terminal == Token_Type.NUM)) and lookahead.type == terminal) or lookahead.lexeme == terminal:  # ID NUM
        Node(str(lookahead))
        print("match", lookahead)
        lookahead = get_next_token(input_file)
    else:
        Syntax_Error(Syntax_Error_Type.MISSING)  # terminal missing


def checkError(currentState):
    global lookahead, rootNode
    if lookahead.lexeme in follow_set[currentState] or lookahead.type.value in follow_set[currentState]:  # synch no epsilon
        print("check error missing", lookahead)
        Syntax_Error(Syntax_Error_Type.MISSING, currentState)
        return False
    else:
        if currentState == "Program":
            rootNode = Node(currentState)
        else:
            Node(currentState)
        print("check error illegal", lookahead)
        Syntax_Error(Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        return True


def checkEpsilonAndError(currentState):
    global lookahead
    if lookahead.lexeme in follow_set[currentState] or lookahead.type.value in follow_set[currentState]:  # currentState -> EPSILON
        Node("epsilon")
        print("check error and epsilon, epsilon", lookahead)
        return False
    else:
        print("check error and epsilon, illegal", lookahead)
        Syntax_Error(Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        return True


def program():
    global lookahead, rootNode
    lookahead = get_next_token(input_file)
    if lookahead.lexeme in first("Declaration-list"):  # Program -> Declaration-list
        print("Program " + str(lookahead))
        declaration_list()
    elif checkError("Program"):
        program()


def declaration_list():
    global lookahead
    if lookahead.lexeme in first("Declaration Declaration-list"):  # Declaration-list -> Declaration Declaration-list
        print("Declaration-list " + str(lookahead))
        declaration()
        declaration_list()
    elif checkEpsilonAndError("Declaration-list"):
        declaration_list()


def declaration():
    global lookahead
    if lookahead.lexeme in first("Declaration-initial Declaration-prime"):  # Declaration -> Declaration-initial Declaration-prime
        print("declaration " + str(lookahead))
        declaration_initial()
        declaration_prime()
    elif checkError("Declaration"):
        declaration()


def declaration_initial():
    global lookahead
    if lookahead.lexeme in first("Type-specifier"):  # Declaration-initial -> Type-specifier ID
        print("declaration-initial " + str(lookahead))
        type_specifier()
        match(Token_Type.ID)
    elif checkError("Declaration-initial"):
        declaration_initial()


def type_specifier():
    global lookahead
    if lookahead.lexeme == "int":  # Type-specifier -> int
        print("Type-specifier " + str(lookahead))
        match("int")
    elif lookahead.lexeme == "void":  # Type-specifier -> void
        print("Type-specifier " + str(lookahead))
        match("void")
    elif checkError("Type-specifier"):
        type_specifier()


def declaration_prime():
    global lookahead
    if lookahead.lexeme in first("Fun-declaration-prime"):  # Declaration-prime -> Fun-declaration-prime
        print("Declaration-prime " + str(lookahead))
        fun_declaration_prime()
    elif lookahead.lexeme in first("Var-declaration-prime"):  # Declaration-prime -> Var_declaration_prime
        print("Declaration-prime " + str(lookahead))
        var_declaration_prime()
    elif checkError("Declaration-prime"):
        declaration_prime()


def fun_declaration_prime():
    global lookahead
    if lookahead.lexeme == "(":  # Fun-declaration-prime -> ( Params ) Compound-stmt
        print("Fun-declaration-prime " + str(lookahead))
        match("(")
        params()
        match(")")
        compound_stmt()
    elif checkError("Fun-declaration-prime"):
        fun_declaration_prime()


def params():
    global lookahead
    if lookahead.lexeme == "int":  # Params -> int ID Param-prime Param-list
        print("Params " + str(lookahead))
        match("int")
        match(Token_Type.ID)
        param_prime()
        param_list()
    elif lookahead.lexeme == "void":  # Params -> void
        print("Params " + str(lookahead))
        match("void")
    elif checkError("Params"):
        params()


def var_declaration_prime():
    global lookahead
    if lookahead.lexeme == ";":  # Var-declaration-prime -> ;
        print("Var-declaration-prime " + str(lookahead))
        match(";")
    elif lookahead.lexeme == "[":  # Var-declaration-prime -> [ NUM ] ;
        print("Var-declaration-prime " + str(lookahead))
        match("[")
        match(Token_Type.NUM)
        match("]")
        match(";")
    elif checkError("Var-declaration-prime"):
        var_declaration_prime()


def param_list():
    global lookahead
    if lookahead.lexeme == ",":  # Param-list -> , Param Param-list
        print("Param-list " + str(lookahead))
        match(",")
        params()
        param_list()
    elif checkEpsilonAndError("Param-list"):
        param_list()


def param_prime():
    global lookahead
    if lookahead.lexeme == "[":  # Param-prime -> [ ]
        print("Param-prime " + str(lookahead))
        match("[")
        match("]")
    elif checkEpsilonAndError("Param-prime"):
        param_prime()


def compound_stmt():
    global lookahead
    if lookahead.lexeme == "{":  # Compound-stmt -> { Declaration-list Statement-list }
        print("Compound-stmt " + str(lookahead))
        match("{")
        declaration_list()
        statement_list()
        match("}")
    elif checkError("Compound-stmt"):
        compound_stmt()


def statement_list():
    global lookahead
    if lookahead.lexeme in first("Statement Statement-list") or lookahead.type.value in first("Statement Statement-list"):  # Statement-list -> Statement Statement-list
        print("Statement-list " + str(lookahead))
        statement()
        statement_list()
    elif checkEpsilonAndError("Statement-list"):
        statement_list()


def expression_stmt():
    global lookahead
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression"):  # Expression-stmt -> Expression ;
        print("Expression-stmt " + str(lookahead))
        expression()
        match(";")
    elif lookahead.lexeme == "break":  # Expression-stmt -> break ;
        print("Expression-stmt " + str(lookahead))
        match("break")
        match(";")
    elif lookahead.lexeme == ";":  # Expression-stmt -> ;
        print("Expression-stmt " + str(lookahead))
        match(";")
    elif checkError("Expression-stmt"):
        expression_stmt()


def selection_stmt():
    global lookahead
    if lookahead.lexeme == "if":  # Selection-stmt -> if ( Expression ) Statement else Statement
        print("Selection-stmt " + str(lookahead))
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
    if lookahead.lexeme == "repeat":  # Iteration-stmt -> repeat Statement until ( Expression )
        print("Iteration-stmt " + str(lookahead))
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
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression"):  # Return-stmt-prime -> Expression ;
        print("Return-stmt-prime " + str(lookahead))
        expression()
        match(";")
    elif lookahead.lexeme == ";":  # Return-stmt-prime -> ;
        print("Return-stmt-prime " + str(lookahead))
        match(";")
    elif checkError("Return-stmt-prime"):
        return_stmt_prime()


def return_stmt():
    global lookahead
    if lookahead.lexeme == "return":  # Return-stmt -> return Return-stmt-prime
        print("Return-stmt " + str(lookahead))
        match("return")
        return_stmt_prime()
    elif checkError("Return-stmt"):
        return_stmt()


def statement():
    global lookahead
    if lookahead.lexeme in first("Expression-stmt") or lookahead.type.value in first("Expression-stmt"):  # Statement -> Expression_stmt
        print("Statement " + str(lookahead))
        expression_stmt()
    elif lookahead.lexeme in first("Compound-stmt") or lookahead.type.value in first("Compound-stmt"):  # Statement -> Compound_stmt
        print("Statement " + str(lookahead))
        compound_stmt()
    elif lookahead.lexeme in first("Selection-stmt") or lookahead.type.value in first("Selection-stmt"):  # Statement -> Selection_stmt
        print("Statement " + str(lookahead))
        selection_stmt()
    elif lookahead.lexeme in first("Iteration-stmt") or lookahead.type.value in first("Iteration-stmt"):  # Statement -> Iteration_stmt
        print("Statement " + str(lookahead))
        iteration_stmt()
    elif lookahead.lexeme in first("Return-stmt") or lookahead.type.value in first("Return-stmt"):  # Statement -> Return_stmt
        print("Statement " + str(lookahead))
        return_stmt()
    elif checkError("Statement"):
        statement()


def simple_expression_zegond():
    global lookahead
    if lookahead.lexeme in first("Additive-expression-zegond C") or lookahead.type.value in first("Additive-expression-zegond C"):  # Simple-expression-zegond -> Additive-expression-zegond C
        print("Simple-expression-zegond " + str(lookahead))
        additive_expression_zegond()
        c()
    elif checkError("Simple-expression-zegond"):
        simple_expression_zegond()


def additive_expression_zegond():
    global lookahead
    if lookahead.lexeme in first("Term-zegond D") or lookahead.type.value in first("Term-zegond D"):  # Additive-expression-zegond -> Term-zegond D
        print("Additive-expression-zegond " + str(lookahead))
        term_zegond()
        d()
    elif checkError("Additive-expression-zegond"):
        additive_expression_zegond()


def expression():
    global lookahead
    if lookahead.lexeme in first("Simple-expression-zegond") or lookahead.type.value in first("Simple-expression-zegond"):  # Expression -> Simple_expression_zegond
        print("Expression " + str(lookahead))
        simple_expression_zegond()
    elif lookahead.type == Token_Type.ID:  # Expression -> ID B
        print("Expression " + str(lookahead))
        match(Token_Type.ID)
        b()
    elif checkError("Expression"):
        expression()


def relop():
    global lookahead
    if lookahead.lexeme == "<":  # Relop -> <
        print("Relop " + str(lookahead))
        match("<")
    elif lookahead.lexeme == "==":  # Relop -> ==
        print("Relop " + str(lookahead))
        match("==")
    elif checkError("Relop"):
        relop()


def c():
    global lookahead
    if lookahead.lexeme in first("Relop Additive-expression") or lookahead.type.value in first("Relop Additive-expression"):  # C -> Relop Additive-expression
        print("C " + str(lookahead))
        relop()
        additive_expression()
    elif checkEpsilonAndError("C"):
        c()


def addop():
    global lookahead
    if lookahead.lexeme == "+":  # Addop -> +
        print("Addop " + str(lookahead))
        match("+")
    elif lookahead.lexeme == "-": # Addop -> -
        print("Addop " + str(lookahead))
        match("-")
    elif checkError("Addop"):
        addop()


def d():
    global lookahead
    if lookahead.lexeme in first("Addop Term D") or lookahead.type.value in first("Addop Term D"):  # D -> Addop Term D
        print("D " + str(lookahead))
        addop()
        term()
        d()
    elif checkEpsilonAndError("D"):
        d()


def term():
    global lookahead
    if lookahead.lexeme in first("Factor G") or lookahead.type.value in first("Factor G"):  # Term -> Factor G
        print("Term " + str(lookahead))
        factor()
        g()
    elif checkError("Term"):
        term()


def g():
    global lookahead
    if lookahead.lexeme == "*":  # G -> * Factor G
        print("G " + str(lookahead))
        match("*")
        factor()
        g()
    elif checkEpsilonAndError("G"):
        g()


def var_call_prime():
    global lookahead
    if lookahead.lexeme == "(":  # Var-call-prime -> ( Args )
        print("Var-call-prime " + str(lookahead))
        match("(")
        args()
        match(")")
    elif lookahead.lexeme in first("Var-prime") or lookahead.type.value in first("Var-prime"):  # Var-call-prime -> Var-prime
        print("Var-call-prime " + str(lookahead))
        var_prime()
    elif checkError("Var-call-prime"):
        var_call_prime()


def factor():
    global lookahead
    if lookahead.lexeme == "(":  # Factor -> ( Expression )
        print("Factor " + str(lookahead))
        match("(")
        expression()
        match(")")
    elif lookahead.type == Token_Type.ID:  # Factor -> ID Var-call-prime
        print("Factor " + str(lookahead))
        match(Token_Type.ID)
        var_call_prime()
    elif lookahead.type.value is Token_Type.NUM:  # Factor -> NUM
        print("Factor " + str(lookahead))
        match(Token_Type.NUM)
    elif checkError("Factor"):
        factor()


def arg_list():
    global lookahead
    if lookahead.lexeme in first("Expression Arg-list-prime") or lookahead.type.value in first("Expression Arg-list-prime"):  # Arg-list -> Expression Arg-list-prime
        print("Arg-list " + str(lookahead))
        expression()
        arg_list_prime()
    elif checkError("Arg-list"):
        arg_list()


def args():
    global lookahead
    if lookahead.lexeme in first("Arg-list") or lookahead.type.value in first("Arg-list"):  # Args -> Arg-list
        print("Args " + str(lookahead))
        arg_list()
    elif checkEpsilonAndError("Args"):
        args()


def arg_list_prime():
    global lookahead
    if lookahead.lexeme == ",":  # Arg-list-prime -> , Expression Arg-list-prime
        print("Arg-list-prime " + str(lookahead))
        match(",")
        expression()
        arg_list_prime()
    elif checkEpsilonAndError("Arg-list-prime"):
        arg_list_prime()


def term_zegond():
    global lookahead
    if lookahead.lexeme in first("Factor-zegond G") or lookahead.type.value in first("Factor-zegond G"):  # Term-zegond -> Factor-zegond G
        print("Term-zegond " + str(lookahead))
        factor_zegond()
        g()
    elif checkError("Term-zegond"):
        term_zegond()


def factor_zegond():
    global lookahead
    if lookahead.lexeme == "(":  # Factor-zegond -> ( Expression )
        print("Factor-zegond " + str(lookahead))
        match("(")
        expression()
        match(")")
    elif lookahead.type == Token_Type.NUM:  # Factor-zegond -> NUM
        print("Factor-zegond " + str(lookahead))
        match(Token_Type.NUM)
    elif checkError("Factor-zegond"):
        factor_zegond()


def b():
    global lookahead
    if lookahead.lexeme == "=":  # B -> = Expression
        print("B " + str(lookahead))
        match("=")
        expression()
    elif lookahead.lexeme == "[":  # B -> [ Expression ] H
        print("B " + str(lookahead))
        match("[")
        expression()
        match("]")
        h()
    elif lookahead.lexeme in first("Simple-expression-prime") or lookahead.type.value in first("Simple-expression-prime"):  # B -> Simple-expression-prime
        print("B " + str(lookahead))
        simple_expression_prime()
    elif checkError("B"):
        b()


def h():
    global lookahead
    if lookahead.lexeme == "=":  # H -> = Expression
        print("H " + str(lookahead))
        match("=")
        expression()
    elif lookahead.lexeme in first("G D C") or lookahead.type.value in first("G D C"):  # H -> G D C
        print("H " + str(lookahead))
        g()
        d()
        c()
    elif checkError("H"):
        h()


def additive_expression():
    global lookahead
    if lookahead.lexeme in first("Term D") or lookahead.type.value in first("Term D"):  # Additive-expression -> Term D
        print("Additive-expression " + str(lookahead))
        term()
        d()
    elif checkError("Additive-expression"):
        additive_expression()


def var_prime():
    global lookahead
    if lookahead.lexeme == "[":  # Var-prime -> [ Expression ]
        print("Var-prime " + str(lookahead))
        match("[")
        expression()
        match("]")
    elif checkEpsilonAndError("Var-prime"):
        var_prime()


def simple_expression_prime():
    global lookahead
    if lookahead.lexeme in first("Additive-expression-prime C") or lookahead.type.value in first("Additive-expression-prime C"):  # Simple-expression-prime -> Additive-expression-prime C
        print("simple_expression_prime " + str(lookahead))
        additive_expression_prime()
        c()
    elif checkError("Simple-expression-prime"):
        simple_expression_prime()


def additive_expression_prime():
    global lookahead
    if lookahead.lexeme in first("Term-prime D") or lookahead.type.value in first("Term-prime D"):  # Additive-expression-prime -> Term-prime D
        print("additive_expression_prime " + str(lookahead))
        term_prime()
        d()
    elif checkError("Additive-expression-prime"):
        additive_expression_prime()


def term_prime():
    global lookahead
    if lookahead.lexeme in first("Factor-prime G") or lookahead.type.value in first("Factor-prime G"):  # Term-prime -> Factor-prime G
        print("Term-prime " + str(lookahead))
        factor_prime()
        g()
    elif checkError("Term-prime"):
        term_prime()


def factor_prime():
    global lookahead
    if lookahead.lexeme == "(":  # Factor-prime -> ( Args )
        print("Factor-prime " + str(lookahead))
        match("(")
        args()
        match(")")
    elif checkEpsilonAndError("Factor-prime"):
        factor_prime()


class Token_Type(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    FINAL = "FINAL"


class Syntax_Error_Type(Enum):
    MISSING = "missing"
    ILLEGAL = "illegal"
    UNEXPECTED_EOF = "Unexpected EOF"


class Syntax_Error:
    def __init__(self, errorType, missingState=""):
        global lookahead
        self.line = lookahead.line
        if errorType == Syntax_Error_Type.UNEXPECTED_EOF:
            self.text = errorType.UNEXPECTED_EOF.value
        elif missingState == "":
            if lookahead.type == Token_Type.ID or lookahead.type == Token_Type.NUM:
                self.text = errorType.value + " " + lookahead.type.value
            else:
                self.text = errorType.value + " " + lookahead.lexeme
        else:  # state missing
            self.text = errorType.value + " " + missingState
        syntax_error_list.append(self)

    def __str__(self):
        return "#" + str(self.line) + " : syntax error, " + self.text


def write_syntax_error():
    file = open("syntax_errors.txt", "w")
    if len(syntax_error_list) != 0:
        for error in syntax_error_list:
            file.write(str(error))
    else:
        file.write("There is no syntax error.")
    file.close()


def write_parse_tree():
    global rootNode
    file = open("parse_tree.txt", "w")
    for pre, fill, node in RenderTree(rootNode):
        file.write("%s%s" % (pre, node.name))
    file.close()


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


class ERROR_Type(Enum):
    INVALID_INPUT = "Invalid input"
    UNCLOSED_COMMENT = "Unclosed comment"
    UNMATCHED_COMMENT = "Unmatched comment"
    INVALID_NUMBER = "Invalid number"


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
        return Token("$", Token_Type.FINAL, 0, False)

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
