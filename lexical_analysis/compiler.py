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
currentState = None
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
    global input_file, lookahead
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Token_Type.KEYWORD, needToAddToTokenList=False)

    
    input_file = open("input.txt", "r")
    
    program()  # parse starts
    write_parse_tree()
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


def match(terminal, parent):
    global lookahead, currentState
    if (((terminal == Token_Type.ID) or (terminal == Token_Type.NUM)) and lookahead.type == terminal) or lookahead.lexeme == terminal:  # ID NUM
        if lookahead.lexeme == '$':
            Node("$", parent)
        else:
            Node(str(lookahead), parent)
            # print("match", lookahead)
            lookahead = get_next_token(input_file)
            # print("next token is: " + str(lookahead))
        
    else:
        Syntax_Error(Syntax_Error_Type.MISSING)  # terminal missing


def checkEpsilonAndError(state, parent):
    global lookahead, rootNode
    if "EPSILON" in first(state):
        if lookahead.lexeme in follow_set[state] or lookahead.type.value in follow_set[state]:  # currentState -> EPSILON
            node = Node(state, parent)
            Node("epsilon", node)
            # print("check error and epsilon, epsilon", lookahead)
            return False
    elif lookahead.lexeme in follow_set[state] or lookahead.type.value in follow_set[state]:  # synch no epsilon
        # print("[[[[[[[[[[[[[[[[[[[[[[[[[[[")
        # print("check error missing", lookahead)
        Syntax_Error(Syntax_Error_Type.MISSING, state)
        return False
    else:
        Node(state, parent="Program")
        #print("check error illegal", lookahead)
        Syntax_Error(Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        return True


def program():
    global lookahead, rootNode
    lookahead = get_next_token(input_file)
    if lookahead.lexeme in first("Declaration-list"):  # Program -> Declaration-list
        rootNode = Node("Program")
        declaration_list(rootNode)
        match("$",rootNode)

    elif checkEpsilonAndError("Program", None):
        program()


def declaration_list(parent_node):
    global lookahead

    if lookahead.lexeme in first("Declaration Declaration-list") or ("EPSILON" not in grammar["Declaration-list"] and "EPSILON" in first("Declaration Declaration-list")):  # Declaration-list -> Declaration Declaration-list
        node = Node("Declaration-list",parent_node)
        declaration(node)
        declaration_list(node)
    elif checkEpsilonAndError("Declaration-list", parent_node):
        declaration_list(parent_node)


def declaration(parent_node):
    global lookahead
    if lookahead.lexeme in first("Declaration-initial Declaration-prime") or ("EPSILON" not in grammar["Declaration"] and "EPSILON" in first("Declaration Declaration-list")):  # Declaration -> Declaration-initial Declaration-prime
        node = Node("Declaration",parent_node)
        declaration_initial(node)
        declaration_prime(node)
    elif checkEpsilonAndError("Declaration", parent_node):
        declaration(parent_node)


def declaration_initial(parent_node):
    global lookahead
    if lookahead.lexeme in first("Type-specifier") or ("EPSILON" not in grammar["Declaration-initial"] and "EPSILON" in first("Type-specifier")):  # Declaration-initial -> Type-specifier ID
        node = Node("Declaration-initial",parent_node)
        type_specifier(node)
        match(Token_Type.ID, node)
    elif checkEpsilonAndError("Declaration-initial", parent_node):
        declaration_initial(node)


def type_specifier(parent_node):
    global lookahead
    if lookahead.lexeme == "int":  # Type-specifier -> int
        node = Node("Type-specifier",parent_node)
        match("int",node)
    elif lookahead.lexeme == "void":  # Type-specifier -> void
        node = Node("Type-specifier",parent_node)
        match("void", node)
    elif checkEpsilonAndError("Type-specifier", parent_node):
        type_specifier(node)


def declaration_prime(parent_node):
    global lookahead
    if lookahead.lexeme in first("Fun-declaration-prime") or ("EPSILON" not in grammar["Declaration-prime"] and "EPSILON" in first("Fun-declaration-prime")):  # Declaration-prime -> Fun-declaration-prime
        node = Node("Declaration-prime",parent_node)
        fun_declaration_prime(node)
    elif lookahead.lexeme in first("Var-declaration-prime") or ("EPSILON" not in grammar["Declaration-prime"] and "EPSILON" in first("Var-declaration-prime")):  # Declaration-prime -> Var_declaration_prime
        node = Node("Declaration-prime",parent_node)
        var_declaration_prime(node)
    elif checkEpsilonAndError("Declaration-prime", parent_node):
        declaration_prime(node)


def fun_declaration_prime(parent_node):
    global lookahead
    # Fun-declaration-prime -> ( Params ) Compound-stmt
    if lookahead.lexeme == "(":
        node = Node("Fun-declaration-prime",parent_node)
        match("(", node)
        params(node)
        match(")", node)
        compound_stmt(node)
    elif checkEpsilonAndError("Fun-declaration-prime", parent_node):
        fun_declaration_prime(node)


def params(parent_node):
    global lookahead
    if lookahead.lexeme == "int":  # Params -> int ID Param-prime Param-list
        node = Node("Params",parent_node)
        match("int", node)
        match(Token_Type.ID, node)
        param_prime(node)
        param_list(node)
    elif lookahead.lexeme == "void":  # Params -> void
        node = Node("Params",parent_node)
        match("void", node)
    elif checkEpsilonAndError("Params", parent_node):
        params(node)



def var_declaration_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ";":  # Var-declaration-prime -> ;
        #print("Var-declaration-prime " + str(lookahead))
        currentState = "Var-declaration-prime"
        node = Node("Var-declaration-prime", parent_node)
        match(";", node)
    elif lookahead.lexeme == "[":  # Var-declaration-prime -> [ NUM ] ;
        #print("Var-declaration-prime " + str(lookahead))
        currentState = "Var-declaration-prime"
        node = Node("Var-declaration-prime", parent_node)
        match("[", node)
        match(Token_Type.NUM, node)
        match("]", node)
        match(";", node)
    elif checkEpsilonAndError("Var-declaration-prime", parent_node):
        var_declaration_prime()


def param_list(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ",":  # Param-list -> , Param Param-list
        #print("Param-list " + str(lookahead))
        currentState = "Param-list"
        node = Node(currentState, parent_node)
        match(",", node)
        params(node)
        param_list(node)
    elif checkEpsilonAndError("Param-list", parent_node):
        param_list()


def param_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "[":  # Param-prime -> [ ]
        #print("Param-prime " + str(lookahead))
        currentState = "Param-prime"
        node = Node(currentState, parent_node)
        match("[", node)
        match("]", node)
    elif checkEpsilonAndError("Param-prime", parent_node):
        param_prime()


def compound_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "{":  # Compound-stmt -> { Declaration-list Statement-list }
        #print("Compound-stmt " + str(lookahead))
        currentState = "Compound-stmt"
        node = Node("Compound-stmt",parent_node)
        match("{", node)
        declaration_list(node)
        statement_list(node)
        match("}", node)
    elif checkEpsilonAndError("Compound-stmt", parent_node):
        compound_stmt()


def statement_list(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Statement Statement-list") or lookahead.type.value in first("Statement Statement-list") or ("EPSILON" not in grammar["Statement-list"] and "EPSILON" in first("Statement Statement-list")):  # Statement-list -> Statement Statement-list
        #print("Statement-list " + str(lookahead))
        currentState = "Statement-list"
        node = Node("Statement-list",parent_node)
        statement(node)
        statement_list(node)
    elif checkEpsilonAndError("Statement-list", parent_node):
        statement_list()


def expression_stmt(parent_node):
    global lookahead, currentState
    
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression") or ("EPSILON" not in grammar["Expression-stmt"] and "EPSILON" in first("Expression")):  # Expression-stmt -> Expression ;
        #print("Expression-stmt " + str(lookahead))
        currentState = "Expression-stmt"
        node = Node("Expression-stmt",parent_node)
        expression(node)
        match(";", node)
    elif lookahead.lexeme == "break":  # Expression-stmt -> break ;
        #print("Expression-stmt " + str(lookahead))
        currentState = "Expression-stmt"
        node = Node("Expression-stmt",parent_node)
        match("break", node)
        match(";", node)
    elif lookahead.lexeme == ";":  # Expression-stmt -> ;
        #print("Expression-stmt " + str(lookahead))
        currentState = "Expression-stmt"
        node = Node("Expression-stmt",parent_node)
        match(";", node)
    elif checkEpsilonAndError("Expression-stmt", parent_node):
        expression_stmt()


def selection_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "if":  # Selection-stmt -> if ( Expression ) Statement else Statement
        #print("Selection-stmt " + str(lookahead))
        currentState = "Selection-stmt"
        node = Node(currentState, parent_node)
        match("if", node)
        match("(", node)
        expression(node)
        match(")", node)
        statement(node)
        match("else", node)
        statement(node)
    elif checkEpsilonAndError("Selection-stmt", parent_node):
        selection_stmt()


def iteration_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "repeat":  # Iteration-stmt -> repeat Statement until ( Expression )
        #print("Iteration-stmt " + str(lookahead))
        currentState = "Iteration-stmt"
        node = Node(currentState, parent_node)
        match("repeat", node)
        statement(node)
        match("until", node)
        match("(", node)
        expression(node)
        match(")", node)
    elif checkEpsilonAndError("Iteration-stmt", parent_node):
        iteration_stmt()


def return_stmt_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression") or ("EPSILON" not in grammar["Return-stmt-prime"] and "EPSILON" in first("Expression")):  # Return-stmt-prime -> Expression ;
        #print("Return-stmt-prime " + str(lookahead))
        currentState = "Return-stmt-prime"
        node = Node(currentState, parent_node)
        expression(node)
        match(";", node)
    elif lookahead.lexeme == ";":  # Return-stmt-prime -> ;
        #print("Return-stmt-prime " + str(lookahead))
        currentState = "Return-stmt-prime"
        node = Node(currentState, parent_node)
        match(";", node)
    elif checkEpsilonAndError("Return-stmt-prime", parent_node):
        return_stmt_prime()


def return_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "return":  # Return-stmt -> return Return-stmt-prime
        #print("Return-stmt " + str(lookahead))
        currentState = "Return-stmt"
        node = Node(currentState, parent_node)
        match("return", node)
        return_stmt_prime(node)
    elif checkEpsilonAndError("Return-stmt", parent_node):
        return_stmt()


def statement(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression-stmt") or lookahead.type.value in first("Expression-stmt") or ("EPSILON" not in grammar["Statement"] and "EPSILON" in first("Expression-stmt")):  # Statement -> Expression_stmt
        #print("Statement " + str(lookahead))
        currentState = "Statement"
        node = Node("Statement",parent_node)
        expression_stmt(node)
    elif lookahead.lexeme in first("Compound-stmt") or lookahead.type.value in first("Compound-stmt")or ("EPSILON" not in grammar["Statement"] and "EPSILON" in first("Compound-stmt")):  # Statement -> Compound_stmt
        #print("Statement " + str(lookahead))
        currentState = "Statement"
        node = Node("Statement",parent_node)
        compound_stmt(node)
    elif lookahead.lexeme in first("Selection-stmt") or lookahead.type.value in first("Selection-stmt")or ("EPSILON" not in grammar["Statement"] and "EPSILON" in first("Selection-stmt")):  # Statement -> Selection_stmt
        #print("Statement " + str(lookahead))
        currentState = "Statement"
        node = Node("Statement",parent_node)
        selection_stmt(node)
    elif lookahead.lexeme in first("Iteration-stmt") or lookahead.type.value in first("Iteration-stmt")or ("EPSILON" not in grammar["Statement"] and "EPSILON" in first("Iteration-stmt")):  # Statement -> Iteration_stmt
       # print("Statement " + str(lookahead))
        currentState = "Statement"
        node = Node("Statement",parent_node)
        iteration_stmt(node)
    elif lookahead.lexeme in first("Return-stmt") or lookahead.type.value in first("Return-stmt")or ("EPSILON" not in grammar["Statement"] and "EPSILON" in first("Return-stmt")):  # Statement -> Return_stmt
        #print("Statement " + str(lookahead))
        currentState = "Statement"
        node = Node("Statement",parent_node)
        return_stmt(node)
    elif checkEpsilonAndError("Statement", parent_node):
        statement()


def simple_expression_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Additive-expression-zegond C") or lookahead.type.value in first("Additive-expression-zegond C") or ("EPSILON" not in grammar["Simple-expression-zegond"] and "EPSILON" in first("Additive-expression-zegond C")):  # Simple-expression-zegond -> Additive-expression-zegond C
        #print("Simple-expression-zegond " + str(lookahead))
        currentState = "Simple-expression-zegond"
        node = Node(currentState, parent_node)
        additive_expression_zegond(node)
        c(node)
    elif checkEpsilonAndError("Simple-expression-zegond", parent_node):
        simple_expression_zegond()


def additive_expression_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term-zegond D") or lookahead.type.value in first("Term-zegond D") or ("EPSILON" not in grammar["Additive-expression-zegond"] and "EPSILON" in first("Term-zegond D")):  # Additive-expression-zegond -> Term-zegond D
        #print("Additive-expression-zegond " + str(lookahead))
        currentState = "Additive-expression-zegond"
        node = Node(currentState, parent_node)
        term_zegond(node)
        d(node)
    elif checkEpsilonAndError("Additive-expression-zegond", parent_node):
        additive_expression_zegond()


def expression(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Simple-expression-zegond") or lookahead.type.value in first("Simple-expression-zegond")  or ("EPSILON" not in grammar["Expression"] and "EPSILON" in first("Simple-expression-zegond")):  # Expression -> Simple_expression_zegond
        #print("Expression " + str(lookahead))
        currentState = "Expression"
        node = Node("Expression",parent_node)
        simple_expression_zegond(node)
    elif lookahead.type == Token_Type.ID:  # Expression -> ID B
        #print("Expression " + str(lookahead))
        currentState = "Expression"
        node = Node("Expression",parent_node)
        match(Token_Type.ID, node)
        b(node)
    elif checkEpsilonAndError("Expression", parent_node):
        expression()


def relop(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "<":  # Relop -> <
        #print("Relop " + str(lookahead))
        currentState = "Relop"
        node = Node(currentState, parent_node)
        match("<", node)
    elif lookahead.lexeme == "==":  # Relop -> ==
        #print("Relop " + str(lookahead))
        currentState = "Relop"
        node = Node(currentState, parent_node)
        match("==", node)
    elif checkEpsilonAndError("Relop", parent_node):
        relop()


def c(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Relop Additive-expression") or lookahead.type.value in first("Relop Additive-expression")  or ("EPSILON" not in grammar["C"] and "EPSILON" in first("Relop Additive-expression")):  # C -> Relop Additive-expression
        #print("C " + str(lookahead))
        currentState = "C"
        node = Node("C",parent_node)
        relop(node)
        additive_expression(node)
    elif checkEpsilonAndError("C", parent_node):
        c()


def addop(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "+":  # Addop -> +
        #print("Addop " + str(lookahead))
        currentState = "Addop"
        node = Node("Addop",parent_node)
        match("+", node)
    elif lookahead.lexeme == "-":  # Addop -> -
        #print("Addop " + str(lookahead))
        currentState = "Addop"
        node = Node("Addop",parent_node)
        match("-", node)
    elif checkEpsilonAndError("Addop", parent_node):
        addop()


def d(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Addop Term D") or lookahead.type.value in first("Addop Term D")  or ("EPSILON" not in grammar["D"] and "EPSILON" in first("Addop Term D")):  # D -> Addop Term D
       # print("D " + str(lookahead))
        currentState = "D"
        node = Node("D",parent_node)
        addop(node)
        term(node)
        d(node)
    elif checkEpsilonAndError("D", parent_node):
        d()


def term(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Factor G") or lookahead.type.value in first("Factor G") or ("EPSILON" not in grammar["Term"] and "EPSILON" in first("Factor G")):  # Term -> Factor G
       # print("Term " + str(lookahead))
        currentState = "Term"
        node = Node("Term",parent_node)
        factor(node)
        g(node)
    elif checkEpsilonAndError("Term", parent_node):
        term()


def g(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "*":  # G -> * Factor G
       # print("G " + str(lookahead))
        currentState = "G"
        node = Node("G",parent_node)
        match("*", node)
        factor(node)
        g(node)
    elif checkEpsilonAndError("G", parent_node):
        g()


def var_call_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Var-call-prime -> ( Args )
        #print("Var-call-prime " + str(lookahead))
        currentState = "Var-call-prime"
        node = Node(currentState, parent_node)
        match("(", node)
        args(node)
        match(")", node)
    elif lookahead.lexeme in first("Var-prime") or lookahead.type.value in first("Var-prime") or ("EPSILON" not in grammar["Var-call-prime"] and "EPSILON" in first("Var-prime")):  # Var-call-prime -> Var-prime
        #print("Var-call-prime " + str(lookahead))
        currentState = "Var-call-prime"
        node = Node(currentState, parent_node)
        var_prime(node)
    elif checkEpsilonAndError("Var-call-prime", parent_node):
        var_call_prime()


def factor(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor -> ( Expression )
        #print("Factor " + str(lookahead))
        currentState = "Factor"
        node = Node("Factor",parent_node)
        match("(", node)
        expression(node)
        match(")", node)
    elif lookahead.type == Token_Type.ID:  # Factor -> ID Var-call-prime
        #print("Factor " + str(lookahead))
        currentState = "Factor"
        node = Node("Factor",parent_node)
        match(Token_Type.ID, node)
        var_call_prime(node)
    elif lookahead.type == Token_Type.NUM:  # Factor -> NUM
        #print("Factor " + str(lookahead))
        currentState = "Factor"
        node = Node("Factor",parent_node)
        match(Token_Type.NUM, node)
    elif checkEpsilonAndError("Factor", parent_node):
        factor()


def arg_list(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression Arg-list-prime") or lookahead.type.value in first("Expression Arg-list-prime") or ("EPSILON" not in grammar["Arg-list"] and "EPSILON" in first("Expression Arg-list-prime")):  # Arg-list -> Expression Arg-list-prime
        #print("Arg-list " + str(lookahead))
        currentState = "Arg-list"
        node = Node(currentState, parent_node)
        expression(node)
        arg_list_prime(node)
    elif checkEpsilonAndError("Arg-list", parent_node):
        arg_list()


def args(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Arg-list") or lookahead.type.value in first("Arg-list") or ("EPSILON" not in grammar["Args"] and "EPSILON" in first("Arg-list")):  # Args -> Arg-list
        #print("Args " + str(lookahead))
        currentState = "Args"
        node = Node(currentState, parent_node)
        arg_list(node)
    elif checkEpsilonAndError("Args", parent_node):
        args()


def arg_list_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ",":  # Arg-list-prime -> , Expression Arg-list-prime
        #print("Arg-list-prime " + str(lookahead))
        currentState = "Arg-list-prime"
        node = Node(currentState, parent_node)
        match(",", node)
        expression(node)
        arg_list_prime(node)
    elif checkEpsilonAndError("Arg-list-prime", parent_node):
        arg_list_prime()


def term_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Factor-zegond G") or lookahead.type.value in first("Factor-zegond G")  or ("EPSILON" not in grammar["Term-zegond"] and "EPSILON" in first("Factor-zegond G")):  # Term-zegond -> Factor-zegond G
        #print("Term-zegond " + str(lookahead))
        currentState = "Term-zegond"
        node = Node(currentState, parent_node)
        factor_zegond(node)
        g(node)
    elif checkEpsilonAndError("Term-zegond", parent_node):
        term_zegond()


def factor_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor-zegond -> ( Expression )
        #print("Factor-zegond " + str(lookahead))
        currentState = "Factor-zegond"
        node = Node(currentState, parent_node)
        match("(", node)
        expression(node)
        match(")", node)
    elif lookahead.type == Token_Type.NUM:  # Factor-zegond -> NUM
        #print("Factor-zegond " + str(lookahead))
        currentState = "Factor-zegond"
        node = Node(currentState, parent_node)
        match(Token_Type.NUM, node)
    elif checkEpsilonAndError("Factor-zegond", parent_node):
        factor_zegond()


def b(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "=":  # B -> = Expression
        #print("B " + str(lookahead))
        currentState = "B"
        node = Node("B",parent_node)
        match("=", node)
        expression(node)
    elif lookahead.lexeme == "[":  # B -> [ Expression ] H
        #print("B " + str(lookahead))
        currentState = "B"
        node = Node("B",parent_node)
        match("[", node)
        expression(node)
        match("]", node)
        h(node)
    elif lookahead.lexeme in first("Simple-expression-prime") or lookahead.type.value in first("Simple-expression-prime")  or ("EPSILON" not in grammar["B"] and "EPSILON" in first("Simple-expression-prime")):  # B -> Simple-expression-prime
        #print("B " + str(lookahead))
        currentState = "B"
        node = Node("B",parent_node)
        simple_expression_prime(node)
    elif checkEpsilonAndError("B", parent_node):
        b()


def h(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "=":  # H -> = Expression
        #print("H " + str(lookahead))
        currentState = "H"
        node = Node(currentState, parent_node)
        match("=", node)
        expression(node)
    elif lookahead.lexeme in first("G D C") or lookahead.type.value in first("G D C")  or ("EPSILON" not in grammar["H"] and "EPSILON" in first("G D C")):  # H -> G D C
        #print("H " + str(lookahead))
        currentState = "H"
        node = Node(currentState, parent_node)
        g(node)
        d(node)
        c(node)
    elif checkEpsilonAndError("H", parent_node):
        h()


def additive_expression(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term D") or lookahead.type.value in first("Term D")  or ("EPSILON" not in grammar["Additive-expression"] and "EPSILON" in first("Term D")):  # Additive-expression -> Term D
        #print("Additive-expression " + str(lookahead))
        currentState = "Additive-expression"
        node = Node(currentState, parent_node)
        term(node)
        d(node)
    elif checkEpsilonAndError("Additive-expression", parent_node):
        additive_expression()


def var_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "[":  # Var-prime -> [ Expression ]
        #print("Var-prime " + str(lookahead))
        currentState = "Var-prime"
        node = Node(currentState, parent_node)
        match("[", node)
        expression(node)
        match("]", node)
    elif checkEpsilonAndError("Var-prime", parent_node):
        var_prime()


def simple_expression_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Additive-expression-prime C") or lookahead.type.value in first("Additive-expression-prime C")  or ("EPSILON" not in grammar["Simple-expression-prime"] and "EPSILON" in first("Additive-expression-prime C")):  # Simple-expression-prime -> Additive-expression-prime C
        #print("simple_expression_prime " + str(lookahead))
        currentState = "Simple-expression-prime"
        node = Node("Simple-expression-prime",parent_node)
        additive_expression_prime(node)
        c(node)
    elif checkEpsilonAndError("Simple-expression-prime", parent_node):
        simple_expression_prime()


def additive_expression_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term-prime D") or lookahead.type.value in first("Term-prime D")  or ("EPSILON" not in grammar["Additive-expression-prime"] and "EPSILON" in first("Term-prime D")):  # Additive-expression-prime -> Term-prime D
        #print("additive_expression_prime " + str(lookahead))
        currentState = "Additive-expression-prime"
        node = Node("Additive-expression-prime",parent_node)
        term_prime(node)
        d(node)
    elif checkEpsilonAndError("Additive-expression-prime", parent_node):
        additive_expression_prime()


def term_prime(parent_node):
    global lookahead, currentState
    #print(first("Factor-prime G"))
    if lookahead.lexeme in first("Factor-prime G") or lookahead.type.value in first("Factor-prime G")  or ("EPSILON" not in grammar["Term-prime"] and "EPSILON" in first("Factor-prime G")):  # Term-prime -> Factor-prime G
        #print("Term-prime " + str(lookahead))
        currentState = "Term-prime"
        node = Node("Term-prime",parent_node)
        factor_prime(node)
        g(node)
    elif checkEpsilonAndError("Term-prime", parent_node):
        term_prime()


def factor_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor-prime -> ( Args )
        #print("Factor-prime " + str(lookahead))
        currentState = "Factor-prime"
        node = Node("Factor-prime",parent_node)
        match("(", node)
        args(node)
        match(")", node)
    elif checkEpsilonAndError("Factor-prime", parent_node):
        factor_prime(node)


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
        for i in range(len(syntax_error_list)):
            if i == len(syntax_error_list) - 1:
                file.write(str(syntax_error_list[i]))
            else:
                file.write(str(syntax_error_list[i]) + "\n")
    else:
        file.write("There is no syntax error.")
    file.close()


def write_parse_tree():
    global rootNode
    
    file = open("parse_tree.txt", "w", encoding="utf-8")
    for pre, _, node in RenderTree(rootNode):
        file.write (("%s%s" % (pre, node.name)) + "\n")
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
