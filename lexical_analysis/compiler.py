from enum import Enum
from anytree import Node, RenderTree

# Alireza Foroodniya 99105645, Foroozan Iraji 99105272
digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
symbols = {";", ":", "{", "}", "[", "]", "(", ")", "<", "+", "-", ","}
keywords = {"break", "else", "if", "int", "repeat", "return", "until", "void"}
symbol_table = []
token_list = []
error_list = []
syntax_error_list = []
three_code_address_list = []
symbol_HashTable = {}
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
semantic_stack = []
tempAddress = 500
dataAddress = 0
ss = {}
currentID = None
pb_pointer = 0


class ACTION(Enum):
    ASSIGN = "ASSIGN"
    ADD = "ADD"
    MULT = "MULT"
    SUB = "SUB"
    EQ = "EQ"
    LT = "LT"
    JPF = "JPF"
    JP = "JP"
    PRINT = "PRINT"
    INITIALIZE = "INITIALIZE"
    MEMORY = "MEMORY"
    PID = "PID"
    OUTPUT = "OUTPUT"
    LESSTHAN = "LESSTHAN"
    PUSHARG = "PUSHARG"


class ADDRESSING_MODE(Enum):
    IMMEDIATE = '#'
    INDIRECT = '@'
    DIRECT = ''


class ThreeCodeAddress:
    def __init__(self, action=ACTION.ASSIGN, num1="", num2="", num3="", addr1=ADDRESSING_MODE.DIRECT, addr2=ADDRESSING_MODE.DIRECT, addr3=ADDRESSING_MODE.DIRECT):
        global pb_pointer
        self.action = action
        self.num1 = num1
        self.num2 = num2
        self.num3 = num3
        self.addr1 = addr1
        self.addr2 = addr2
        self.addr3 = addr3
        three_code_address_list.append(self)
        pb_pointer += 1

    def __str__(self):
        return "(" + self.action.value + ", " + str(self.addr1.value) + str(self.num1) + ", " + \
            str(self.addr2.value) + str(self.num2) + ", " + str(self.addr3.value) + str(self.num3) + " )"


def getTemp():
    global tempAddress
    x = tempAddress
    tempAddress += 4
    return x


def memory():
    # (ASSIGN, #4, 0,   )
    # (JP, 2,  ,   )
    getTemp()
    ThreeCodeAddress(ACTION.ASSIGN, "4", "0", addr1=ADDRESSING_MODE.IMMEDIATE)
    getTemp()
    ThreeCodeAddress(ACTION.JP, "2")


def initialize():
    # (ASSIGN, #0, t,   )
    global currentID
    print(currentID.lexeme)
    t = getTemp()
    setattr(currentID, 'address', t)
    #currentID.address = t
    print(currentID.address)
    ThreeCodeAddress(ACTION.ASSIGN, "0", str(t), addr1=ADDRESSING_MODE.IMMEDIATE)


def assign():
    ThreeCodeAddress(ACTION.ASSIGN, )
    return 0


def output():
    print(semantic_stack)
    ThreeCodeAddress(ACTION.PRINT, semantic_stack.pop())


def pushArg():
    global currentID
    print(";;;;;;;;;")
    print(getattr(currentID, 'address'))
    semantic_stack.append(currentID.address)


def pid():
    global currentID

    return 0


def mult():
    ThreeCodeAddress(ACTION.MULT, "#0", getTemp())
    return 0


def add():
    ThreeCodeAddress(ACTION.ADD, "#0", getTemp())
    return 0


def sub():
    ThreeCodeAddress(ACTION.SUB, "#0", getTemp())
    return 0


def checkOutput():
    return 0


def lessThan():
    # (LT, A1, A2, R )
  #  ThreeCodeAddress(ACTION.LT, str(getTemp()), semantic_stack.pop(), semantic_stack.pop())
  return 0


def equal():
    # (EQ, A1, A2, R )
    ThreeCodeAddress(ACTION.EQ, str(getTemp()), semantic_stack.pop(), semantic_stack.pop())


def jumpOnFalse():
    # (JPF, A, L, )
    ThreeCodeAddress(ACTION.JPF, str(getTemp()), semantic_stack.pop(), semantic_stack.pop())


def code_gen(action):
    if action == ACTION.PID:
        pid()
    elif action == ACTION.MULT:
        mult()
    elif action == ACTION.ADD:
        add()
    elif action == ACTION.ASSIGN:
        assign()
    elif action == ACTION.INITIALIZE:
        initialize()
    elif action == ACTION.MEMORY:
        memory()
    elif action == ACTION.OUTPUT:
        output()
    elif action == ACTION.LESSTHAN:
        lessThan()
    elif action == ACTION.PUSHARG:
        pushArg()


def main():
    global input_file, lookahead
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Token_Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
    program()
    symbol_writer()
    write_parse_tree()
    write_three_code_address()
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
        if string in grammar.keys():
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


def match(terminal, parent):
    global lookahead, currentState, currentID
    if terminal == "$":
        Node("$", parent)
    elif ((terminal == Token_Type.ID or terminal == Token_Type.NUM) and lookahead.type == terminal) or lookahead.lexeme == terminal:  # ID NUM
        if lookahead.lexeme == "$":
            if terminal != "$":
                Syntax_Error(Syntax_Error_Type.UNEXPECTED_EOF)
            else:
                Node("$", parent)
        else:
            Node(str(lookahead), parent)
            if terminal == Token_Type.ID:
                currentID = lookahead
            lookahead = get_next_token(input_file)
    else:
        if terminal == Token_Type.ID or terminal == Token_Type.NUM:
            missing = terminal.value
        else:
            missing = terminal
        Syntax_Error(Syntax_Error_Type.MISSING, missing)  # terminal missing


def checkError(state, haveEpsilon=False, parent=None):
    global lookahead
    if haveEpsilon:
        node = Node(state, parent)
        Node("epsilon", node)
    elif lookahead.lexeme in follow_set[state] or lookahead.type.value in follow_set[state]:  # synch
        if haveEpsilon:
            node = Node(state, parent)
            Node("epsilon", node)
        else:
            Syntax_Error(Syntax_Error_Type.MISSING, state)
    else:  # empty cells in parse table
        Syntax_Error(Syntax_Error_Type.ILLEGAL)
        lookahead = get_next_token(input_file)
        return True
    return False


def program():
    global lookahead, rootNode, currentState
    lookahead = get_next_token(input_file)
    if lookahead.lexeme in first("Declaration-list"):  # Program -> #memory Declaration-list
        currentState = "Program"
        rootNode = Node(currentState)
        code_gen(ACTION.MEMORY)
        declaration_list(rootNode)
    elif "EPSILON" in first("Declaration-list") and (lookahead.lexeme in follow_set["Program"] or lookahead.type.value in follow_set["Program"]):
        node = Node(state, parent)
        Node("epsilon", rootNode)
    elif checkError("Program"):
        program()


def declaration_list(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Declaration Declaration-list"):  # Declaration-list -> Declaration Declaration-list
        currentState = "Declaration-list"
        node = Node(currentState, parent_node)
        declaration(node)
        declaration_list(node)
    elif "EPSILON" in first("Declaration Declaration-list") and (lookahead.lexeme in follow_set["Declaration-list"] or lookahead.type.value in follow_set["Declaration-list"]):
        Node("epsilon", rootNode)
    elif checkError("Declaration-list", True, parent_node):
        declaration_list(parent_node)


def declaration(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Declaration-initial Declaration-prime"):  # Declaration -> Declaration-initial Declaration-prime
        currentState = "Declaration"
        node = Node(currentState, parent_node)
        declaration_initial(node)
        declaration_prime(node)
    elif checkError("Declaration"):
        declaration(parent_node)


def declaration_initial(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Type-specifier"):  # Declaration-initial -> Type-specifier ID
        currentState = "Declaration-initial"
        node = Node(currentState, parent_node)
        type_specifier(node)
        match(Token_Type.ID, node)
        code_gen(ACTION.PID)
    elif checkError("Declaration-initial"):
        declaration_initial(parent_node)


def type_specifier(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "int":  # Type-specifier -> int
        currentState = "Type-specifier"
        node = Node(currentState, parent_node)
        match("int", node)
    elif lookahead.lexeme == "void":  # Type-specifier -> void
        currentState = "Type-specifier"
        node = Node(currentState, parent_node)
        match("void", node)
    elif checkError("Type-specifier"):
        type_specifier(parent_node)


def declaration_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Fun-declaration-prime"):  # Declaration-prime -> Fun-declaration-prime
        currentState = "Declaration-prime"
        node = Node(currentState, parent_node)
        fun_declaration_prime(node)
    elif lookahead.lexeme in first("Var-declaration-prime"):  # Declaration-prime -> Var_declaration_prime #initialize
        currentState = "Declaration-prime"
        node = Node(currentState, parent_node)
        var_declaration_prime(node)
        code_gen(ACTION.INITIALIZE)
    elif checkError("Declaration-prime"):
        declaration_prime(parent_node)


def fun_declaration_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Fun-declaration-prime -> ( Params ) Compound-stmt
        currentState = "Fun-declaration-prime"
        node = Node(currentState, parent_node)
        match("(", node)
        params(node)
        match(")", node)
        compound_stmt(node)
    elif checkError("Fun-declaration-prime"):
        fun_declaration_prime(parent_node)


def params(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "int":  # Params -> int ID Param-prime Param-list
        currentState = "Params"
        node = Node(currentState, parent_node)
        match("int", node)
        match(Token_Type.ID, node)
        param_prime(node)
        param_list(node)
    elif lookahead.lexeme == "void":  # Params -> void
        currentState = "Params"
        node = Node(currentState, parent_node)
        match("void", node)
    elif checkError("Params"):
        params(parent_node)


def var_declaration_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ";":  # Var-declaration-prime -> ;
        currentState = "Var-declaration-prime"
        node = Node(currentState, parent_node)
        match(";", node)
    elif lookahead.lexeme == "[":  # Var-declaration-prime -> [ NUM ] ;
        currentState = "Var-declaration-prime"
        node = Node(currentState, parent_node)
        match("[", node)
        match(Token_Type.NUM, node)
        match("]", node)
        match(";", node)
    elif checkError("Var-declaration-prime"):
        var_declaration_prime(parent_node)


def param_list(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ",":  # Param-list -> , Param Param-list
        currentState = "Param-list"
        node = Node(currentState, parent_node)
        match(",", node)
        params(node)
        param_list(node)
    elif checkError("Param-list", True, parent_node):
        param_list(parent_node)


def param_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "[":  # Param-prime -> [ ]
        currentState = "Param-prime"
        node = Node(currentState, parent_node)
        match("[", node)
        match("]", node)
    elif checkError("Param-prime", True, parent_node):
        param_prime(parent_node)


def compound_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "{":  # Compound-stmt -> { Declaration-list Statement-list }
        currentState = "Compound-stmt"
        node = Node(currentState, parent_node)
        match("{", node)
        declaration_list(node)
        statement_list(node)
        match("}", node)
    elif checkError("Compound-stmt"):
        compound_stmt(parent_node)


def statement_list(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Statement Statement-list") or lookahead.type.value in first("Statement Statement-list"):  # Statement-list -> Statement Statement-list
        currentState = "Statement-list"
        node = Node(currentState, parent_node)
        statement(node)
        statement_list(node)
    elif checkError("Statement-list", True, parent_node):
        statement_list(parent_node)


def expression_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression"):  # Expression-stmt -> Expression ;
        currentState = "Expression-stmt"
        node = Node(currentState, parent_node)
        expression(node)
        match(";", node)
    elif lookahead.lexeme == "break":  # Expression-stmt -> break ;
        currentState = "Expression-stmt"
        node = Node(currentState, parent_node)
        match("break", node)
        match(";", node)
    elif lookahead.lexeme == ";":  # Expression-stmt -> ;
        currentState = "Expression-stmt"
        node = Node(currentState, parent_node)
        match(";", node)
    elif checkError("Expression-stmt"):
        expression_stmt(parent_node)


def selection_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "if":  # Selection-stmt -> if ( Expression ) Statement else Statement
        currentState = "Selection-stmt"
        node = Node(currentState, parent_node)
        match("if", node)
        match("(", node)
        expression(node)
        match(")", node)
        statement(node)
        match("else", node)
        statement(node)
    elif checkError("Selection-stmt"):
        selection_stmt(parent_node)


def iteration_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "repeat":  # Iteration-stmt -> repeat Statement until ( Expression )
        currentState = "Iteration-stmt"
        node = Node(currentState, parent_node)
        match("repeat", node)
        statement(node)
        match("until", node)
        match("(", node)
        expression(node)
        match(")", node)
    elif checkError("Iteration-stmt"):
        iteration_stmt(parent_node)


def return_stmt_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first("Expression"):  # Return-stmt-prime -> Expression ;
        currentState = "Return-stmt-prime"
        node = Node(currentState, parent_node)
        expression(node)
        match(";", node)
    elif lookahead.lexeme == ";":  # Return-stmt-prime -> ;
        currentState = "Return-stmt-prime"
        node = Node(currentState, parent_node)
        match(";", node)
    elif checkError("Return-stmt-prime"):
        return_stmt_prime(parent_node)


def return_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "return":  # Return-stmt -> return Return-stmt-prime
        currentState = "Return-stmt"
        node = Node(currentState, parent_node)
        match("return", node)
        return_stmt_prime(node)
    elif checkError("Return-stmt"):
        return_stmt(parent_node)


def statement(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression-stmt") or lookahead.type.value in first("Expression-stmt"):  # Statement -> Expression_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        expression_stmt(node)
    elif lookahead.lexeme in first("Compound-stmt") or lookahead.type.value in first("Compound-stmt"):  # Statement -> Compound_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        compound_stmt(node)
    elif lookahead.lexeme in first("Selection-stmt") or lookahead.type.value in first("Selection-stmt"):  # Statement -> Selection_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        selection_stmt(node)
    elif lookahead.lexeme in first("Iteration-stmt") or lookahead.type.value in first("Iteration-stmt"):  # Statement -> Iteration_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        iteration_stmt(node)
    elif lookahead.lexeme in first("Return-stmt") or lookahead.type.value in first("Return-stmt"):  # Statement -> Return_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        return_stmt(node)
    elif checkError("Statement"):
        statement(parent_node)


def simple_expression_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Additive-expression-zegond C") or lookahead.type.value in first("Additive-expression-zegond C"):  # Simple-expression-zegond -> Additive-expression-zegond C
        currentState = "Simple-expression-zegond"
        node = Node(currentState, parent_node)
        additive_expression_zegond(node)
        c(node)
    elif checkError("Simple-expression-zegond"):
        simple_expression_zegond(parent_node)


def additive_expression_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term-zegond D") or lookahead.type.value in first("Term-zegond D"):  # Additive-expression-zegond -> Term-zegond D
        currentState = "Additive-expression-zegond"
        node = Node(currentState, parent_node)
        term_zegond(node)
        d(node)
    elif checkError("Additive-expression-zegond"):
        additive_expression_zegond(parent_node)


def expression(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Simple-expression-zegond") or lookahead.type.value in first("Simple-expression-zegond"):  # Expression -> Simple_expression_zegond
        currentState = "Expression"
        node = Node(currentState, parent_node)
        simple_expression_zegond(node)
    elif lookahead.type == Token_Type.ID:  # Expression -> ID B
        currentState = "Expression"
        node = Node(currentState, parent_node)
        match(Token_Type.ID, node)
        b(node)
    elif checkError("Expression"):
        expression(parent_node)


def relop(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "<":  # Relop -> < #lessThan
        currentState = "Relop"
        node = Node(currentState, parent_node)
        match("<", node)
        code_gen(ACTION.LESSTHAN)
    elif lookahead.lexeme == "==":  # Relop -> ==
        currentState = "Relop"
        node = Node(currentState, parent_node)
        match("==", node)
    elif checkError("Relop"):
        relop(parent_node)


def c(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Relop Additive-expression") or lookahead.type.value in first("Relop Additive-expression"):  # C -> Relop Additive-expression
        currentState = "C"
        node = Node("C", parent_node)
        relop(node)
        additive_expression(node)
    elif checkError("C", True, parent_node):
        c(parent_node)


def addop(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "+":  # Addop -> + #add
        currentState = "Addop"
        node = Node(currentState, parent_node)
        match("+", node)
        #code_gen(ACTION.ADD)
    elif lookahead.lexeme == "-":  # Addop -> - #sub
        currentState = "Addop"
        node = Node(currentState, parent_node)
        match("-", node)
        #code_gen(ACTION.SUB)
    elif checkError("Addop"):
        addop(parent_node)


def d(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Addop Term D") or lookahead.type.value in first("Addop Term D"):  # D -> Addop Term D
        currentState = "D"
        node = Node(currentState, parent_node)
        addop(node)
        term(node)
        d(node)
    elif checkError("D", True, parent_node):
        d(parent_node)


def term(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Factor G") or lookahead.type.value in first("Factor G"):  # Term -> Factor G
        currentState = "Term"
        node = Node(currentState, parent_node)
        factor(node)
        g(node)
    elif checkError("Term"):
        term(parent_node)


def g(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "*":  # G -> * Factor G
        currentState = "G"
        node = Node(currentState, parent_node)
        match("*", node)
        factor(node)
        g(node)
    elif checkError("G", True, parent_node):
        g(parent_node)


def var_call_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Var-call-prime -> ( Args )
        currentState = "Var-call-prime"
        node = Node(currentState, parent_node)
        match("(", node)
        args(node)
        match(")", node)
    elif lookahead.lexeme in first("Var-prime") or lookahead.type.value in first("Var-prime"):  # Var-call-prime -> Var-prime
        currentState = "Var-call-prime"
        node = Node(currentState, parent_node)
        var_prime(node)
    elif checkError("Var-call-prime"):
        var_call_prime(parent_node)


def factor(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor -> ( Expression )
        currentState = "Factor"
        node = Node(currentState, parent_node)
        match("(", node)
        expression(node)
        match(")", node)
    elif lookahead.type == Token_Type.ID:  # Factor -> ID Var-call-prime
        currentState = "Factor"
        node = Node(currentState, parent_node)
        match(Token_Type.ID, node)
        var_call_prime(node)
    elif lookahead.type == Token_Type.NUM:  # Factor -> NUM
        currentState = "Factor"
        node = Node(currentState, parent_node)
        match(Token_Type.NUM, node)
    elif checkError("Factor"):
        factor(parent_node)


def arg_list(parent_node):
    global lookahead, currentState, currentID
    if lookahead.lexeme in first("Expression Arg-list-prime") or lookahead.type.value in first("Expression Arg-list-prime"):  # Arg-list -> Expression #pushArg Arg-list-prime
        currentState = "Arg-list"
        node = Node(currentState, parent_node)
        expression(node)
        code_gen(ACTION.PUSHARG)
        arg_list_prime(node)
    elif checkError("Arg-list"):
        arg_list(parent_node)


def args(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Arg-list") or lookahead.type.value in first("Arg-list"):  # Args -> Arg-list
        currentState = "Args"
        node = Node(currentState, parent_node)
        arg_list(node)
    elif checkError("Args", True, parent_node):
        args(parent_node)


def arg_list_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ",":  # Arg-list-prime -> , Expression Arg-list-prime
        currentState = "Arg-list-prime"
        node = Node(currentState, parent_node)
        match(",", node)
        expression(node)
        arg_list_prime(node)
    elif checkError("Arg-list-prime", True, parent_node):
        arg_list_prime(parent_node)


def term_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Factor-zegond G") or lookahead.type.value in first("Factor-zegond G"):  # Term-zegond -> Factor-zegond G
        currentState = "Term-zegond"
        node = Node(currentState, parent_node)
        factor_zegond(node)
        g(node)
    elif checkError("Term-zegond"):
        term_zegond(parent_node)


def factor_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor-zegond -> ( Expression )
        currentState = "Factor-zegond"
        node = Node(currentState, parent_node)
        match("(", node)
        expression(node)
        match(")", node)
    elif lookahead.type == Token_Type.NUM:  # Factor-zegond -> NUM
        currentState = "Factor-zegond"
        node = Node(currentState, parent_node)
        match(Token_Type.NUM, node)
    elif checkError("Factor-zegond"):
        factor_zegond(parent_node)


def b(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "=":  # B -> = Expression
        currentState = "B"
        node = Node(currentState, parent_node)
        match("=", node)
        expression(node)
    elif lookahead.lexeme == "[":  # B -> [ Expression ] H
        currentState = "B"
        node = Node(currentState, parent_node)
        match("[", node)
        expression(node)
        match("]", node)
        h(node)
    elif lookahead.lexeme in first("Simple-expression-prime") or lookahead.type.value in first("Simple-expression-prime"):  # B -> Simple-expression-prime
        currentState = "B"
        node = Node(currentState, parent_node)
        simple_expression_prime(node)
    elif checkError("B"):
        b(parent_node)


def h(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "=":  # H -> = Expression
        currentState = "H"
        node = Node(currentState, parent_node)
        match("=", node)
        expression(node)
    elif lookahead.lexeme in first("G D C") or lookahead.type.value in first("G D C"):  # H -> G D C
        currentState = "H"
        node = Node(currentState, parent_node)
        g(node)
        d(node)
        c(node)
    elif checkError("H"):
        h(parent_node)


def additive_expression(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term D") or lookahead.type.value in first("Term D"):  # Additive-expression -> Term D
        currentState = "Additive-expression"
        node = Node(currentState, parent_node)
        term(node)
        d(node)
    elif checkError("Additive-expression"):
        additive_expression(parent_node)


def var_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "[":  # Var-prime -> [ Expression ]
        currentState = "Var-prime"
        node = Node(currentState, parent_node)
        match("[", node)
        expression(node)
        match("]", node)
    elif checkError("Var-prime", True, parent_node):
        var_prime(parent_node)


def simple_expression_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Additive-expression-prime C") or lookahead.type.value in first("Additive-expression-prime C"):  # Simple-expression-prime -> Additive-expression-prime C
        currentState = "Simple-expression-prime"
        node = Node(currentState, parent_node)
        additive_expression_prime(node)
        c(node)
    elif checkError("Simple-expression-prime"):
        simple_expression_prime(parent_node)


def additive_expression_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term-prime D") or lookahead.type.value in first("Term-prime D"):  # Additive-expression-prime -> Term-prime D
        currentState = "Additive-expression-prime"
        node = Node(currentState, parent_node)
        term_prime(node)
        d(node)
    elif checkError("Additive-expression-prime"):
        additive_expression_prime(parent_node)


def term_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Factor-prime G") or lookahead.type.value in first("Factor-prime G"):  # Term-prime -> Factor-prime G
        currentState = "Term-prime"
        node = Node(currentState, parent_node)
        factor_prime(node)
        g(node)
    elif checkError("Term-prime"):
        term_prime(parent_node)


def factor_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor-prime -> ( Args #output )
        currentState = "Factor-prime"
        node = Node(currentState, parent_node)
        match("(", node)
        args(node)
        match(")", node)
        code_gen(ACTION.OUTPUT)
    elif checkError("Factor-prime", True, parent_node):
        factor_prime(parent_node)


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


class Token:
    def __init__(self, lexeme="", type=Token_Type.ID, line=0, needToAddToTokenList=True):
        self._address = None
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.address = None
        if (type == Token_Type.ID or type == Token_Type.KEYWORD) and lexeme not in symbol_table:
            symbol_table.append(self)
            symbol_HashTable[lexeme] = self
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
    for i in range(len(symbol_table)):
        file.write(str(i + 1) + ".\t" + symbol_table[i].lexeme + "\n")
    file.close()


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
        file.write(("%s%s" % (pre, node.name)) + "\n")
    file.close()


def write_three_code_address():
    global three_code_address_list
    file = open("output.txt", "w")
    if len(three_code_address_list) != 0:
        for i in range(len(three_code_address_list)):
            file.write(str(i) + "\t" + str(three_code_address_list[i]) + "\n")
    else:
        file.write("")
    file.close()


main()
