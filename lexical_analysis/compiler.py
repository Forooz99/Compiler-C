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
semantic_error_list = []
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
semantic_stack = []
tempAddress = 500
pb_pointer = 0
scopeNumber = 0
previousToken = None


def main():
    global input_file, lookahead
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Token_Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")
    program()
    write_parse_tree()
    write_three_code_address()
    write_semantic_error()
    input_file.close()


# ########## Semantic ########## #
class Semantic_Error:
    def __init__(self, token, text):
        self.line = token.line
        self.text = text
        semantic_error_list.append(self)

    def __str__(self):
        return "#" + str(self.line) + ": Semantic Error! " + self.text


class SEMANTIC_ACTION(Enum):
    SCOPING = 1
    VARTYPE = 2
    PARAMNUM = 3
    BREAK = 4
    TYPEMISMATCH = 5
    PARAMTYPE = 6


def semantic_check(action):
   return
    # if action == SEMANTIC_ACTION.VARTYPE:
    #     varType()
    # elif action == SEMANTIC_ACTION.SCOPING:
    #     scoping()
    # elif action == SEMANTIC_ACTION.PARAMNUM:
    #     paramNum()
    # elif action == SEMANTIC_ACTION.BREAK:
    #     doBreak()
    # elif action == SEMANTIC_ACTION.TYPEMISMATCH:
    #     typeMismatch()
    # elif action == SEMANTIC_ACTION.PARAMTYPE:
    #     paramType()


def varType():
    token = semantic_stack.pop()
    type = semantic_stack.pop()
    if type.lexeme == "void":
        Semantic_Error(token, "Illegal type of void for '" + token.lexeme + "'.")


def scoping():
    global lookahead
    if lookahead.lexeme != "output" and getVarTypeOfToken(lookahead.lexeme) == "":
        Semantic_Error(lookahead, "'" + lookahead.lexeme + "' is not defined.")


def paramNum():
    token = semantic_stack.pop()
    Semantic_Error(token, "Mismatch in numbers of arguments of '" + token.lexeme + "'.")


def doBreak():
    global lookahead
    token = lookahead
    Semantic_Error(token, "No 'repeat ... until' found for 'break'.")


def typeMismatch():
    return 0


def paramType():
    return 0


def write_semantic_error():
    file = open("semantic_errors.txt", "w")
    if len(semantic_error_list) != 0:
        for i in range(len(semantic_error_list)):
            if i == len(semantic_error_list) - 1:
                file.write(str(semantic_error_list[i]))
            else:
                file.write(str(semantic_error_list[i]) + "\n")
    else:
        file.write("The input program is semantically correct.")
    file.close()


# ########## Code Generation ########## #
class ACTION(Enum):
    BYTE = "BYTE"
    MAINFUN = "MAINFUN"
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
    PUSHID = "PUSHID"
    LESSTHAN = "LESSTHAN"
    EXPRESSION = "EXPRESSION"
    SAVE = "SAVE"
    JPFSAVE = "JPFSAVE"
    RELOP = "RELOP"
    JPSAVE = "JPSAVE"
    LABEL = "LABEL"
    JPMAKEGAP = "JPMAKEGAP"
    JPBREAK = "JPBREAK"
    JPFUNTIL = "JPFUNTIL"
    ARRAY = "ARRAY"
    SETADDRESS = "SETADDRESS"
    FUNDECLARE = "FUNDECLARE"
    ALLOCATE_SAVE_AREA = "ALLOCATE_SAVE_AREA_AND_RETURN_AND_RESULT"  # put the save address up for function to use and allocate some space for result
    SAVE_ARG = "SAVE_ARG"  # save the args for func
    SAVE_RETURN_AND_JUMP = "SAVE_RETURN_AND_JUMP"
    GOTO_SAVE_AREA = "GOTO_SAVE_AREA"
    READ_VALUE = "READ_VALUE"


class ADDRESSING_MODE(Enum):
    IMMEDIATE = '#'
    INDIRECT = '@'
    DIRECT = ''


class ThreeCodeAddress:
    def __init__(self, action=ACTION.ASSIGN, num1=" ", num2=" ", num3=" ", addr1=ADDRESSING_MODE.DIRECT,
                 addr2=ADDRESSING_MODE.DIRECT, addr3=ADDRESSING_MODE.DIRECT):
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
        return "(" + self.action.value + ", " + str(self.num1) + ", " + str(self.num2) + ", " + str(self.num3) + " )"


def getTemp(a=1):
    global tempAddress
    x = tempAddress
    tempAddress += (a * 4)
    return x


def getParameter(t):  # for defining addressing Mode
    if type(t) is Token:
        if t.type == Token_Type.ID:
            return str(getTempOfToken(t.lexeme))
        elif t.type == Token_Type.NUM:
            return "#" + t.lexeme
    else:
        return t


def code_gen(action):
    if action == ACTION.MAINFUN:
        mainFun()
    elif action == ACTION.PUSHID:
        pushId()
    elif action == ACTION.INITIALIZE:
        initialize()
    elif action == ACTION.ARRAY:
        array()
    elif action == ACTION.ASSIGN:
        assign()
    elif action == ACTION.PRINT:
        output()
    elif action == ACTION.SETADDRESS:
        setAddress()
    elif action == ACTION.EXPRESSION:
        doExpression()
    elif action == ACTION.LESSTHAN:
        lessThan()
    elif action == ACTION.RELOP:
        doRelop()
    elif action == ACTION.SAVE:
        save()
    elif action == ACTION.JPF:
        jumpOnFalse()
    elif action == ACTION.JP:
        jump()
    elif action == ACTION.JPFSAVE:
        jpf_save()
    elif action == ACTION.JPSAVE:
        jp_save()
    elif action == ACTION.LABEL:
        label()
    elif action == ACTION.JPMAKEGAP:
        jump_and_make_gap()
    elif action == ACTION.JPBREAK:
        jump_for_break()
    elif action == ACTION.JPFUNTIL:
        jump_until()
    elif action == ACTION.BYTE:
        byte()
    elif action == ACTION.FUNDECLARE:
        funDeclare()
    elif action == ACTION.ALLOCATE_SAVE_AREA:
        allocate_save_area()
    elif action == ACTION.SAVE_ARG:
        save_arg()
    elif action == ACTION.SAVE_RETURN_AND_JUMP:
        save_return_and_jump()
    elif action == ACTION.GOTO_SAVE_AREA:
        goto_save_area()
    elif action == ACTION.READ_VALUE:
        read_value()


def goto_save_area():
    global save_area_temp, distance_from_save
    save_area_temp = getTemp()
    ThreeCodeAddress(ACTION.ASSIGN, str(6000), last_temp)
    distance_from_save = 4
    return


def read_value():
    global distance_from_save
    x = getTemp()
    ThreeCodeAddress(ACTION.ADD, save_area_temp, "#" + str(distance_from_save), x)
    distance_from_save += 4
    ThreeCodeAddress(ACTION.ASSIGN, "@" + str(x), getTempOfToken(previousToken.lexeme))
    return


def allocate_save_area():
    global function_pointer, start_of_save_area
    ThreeCodeAddress(ACTION.ASSIGN, "#" + str(start_of_save_area), str(function_pointer))
    start_of_save_area += 4


def save_arg():
    global start_of_save_area
    argument = semantic_stack.pop()
    if argument.type == Token_Type.NUM:
        ThreeCodeAddress(ACTION.ASSIGN, "#" + argument.lexeme, str(start_of_save_area))
    elif argument.type == Token_Type.ID:
        ThreeCodeAddress(ACTION.ASSIGN, getParameter(argument), str(start_of_save_area))
    start_of_save_area += 4


def save_return_and_jump():
    global start_of_save_area
    ThreeCodeAddress(ACTION.ASSIGN, str(pb_pointer + 2), str(start_of_save_area))
    start_of_save_area += 4
    # ThreeCodeAddress(ACTION.JP, )


def byte():
    ThreeCodeAddress(ACTION.ASSIGN, "#4", "0", addr1=ADDRESSING_MODE.IMMEDIATE)


def mainFun():
    ThreeCodeAddress(ACTION.JP, str(pb_pointer + 1))


def pushId(): #debug
    if lookahead.lexeme != "main" and lookahead.lexeme != "output":
        semantic_stack.append(lookahead)


def initialize():
    temp = getTemp()
    identifier = semantic_stack.pop()
    type = semantic_stack[-1]
    setVarTypeForToken(identifier.lexeme, type.lexeme)
    setTempForToken(identifier.lexeme, temp)  # add address to symbol tbl
    ThreeCodeAddress(ACTION.ASSIGN, "#0", str(temp))
    setScope(identifier.lexeme, scopeNumber)
    semantic_stack.append(identifier)  # for semantic check


def setAddress():
    temp = getTemp()
    index = semantic_stack.pop()
    identifier = semantic_stack.pop()
    ThreeCodeAddress(ACTION.MULT, getParameter(index), "#4", str(temp))
    ThreeCodeAddress(ACTION.ADD, "#" + getParameter(identifier), str(temp), str(temp))
    semantic_stack.append("@" + str(temp))


def array():
    a = semantic_stack.pop()
    temp = getTemp(int(a.lexeme))
    identifier = semantic_stack.pop()
    type = semantic_stack[-1]
    setVarTypeForToken(identifier.lexeme, type.lexeme)
    setTempForToken(identifier.lexeme, temp)  # add address to symbol tbl
    ThreeCodeAddress(ACTION.ASSIGN, "#0", str(temp))
    semantic_stack.append(identifier)  # for semantic check


def assign(): #debug
    global semantic_stack
    t1 = semantic_stack.pop()
    #t2 = semantic_stack.pop()
    ThreeCodeAddress(ACTION.ASSIGN, getParameter(t1), getParameter(semantic_stack[-1]))


def output(): #debug
    #t = semantic_stack.pop()
    ThreeCodeAddress(ACTION.PRINT, getParameter(semantic_stack[-1]))


def pushSymbol():
    semantic_stack.append(currentSymbol)


def jump():
    return


def doExpression():
    symbol = semantic_stack.pop(-2)
    if symbol.lexeme == "+":
        add()
    elif symbol.lexeme == "-":
        sub()
    elif symbol.lexeme == "*":
        mult()


def doRelop():
    symbol = semantic_stack.pop(-2)
    if symbol.lexeme == "<":
        lessThan()
    elif symbol.lexeme == "==":
        equal()


def add():
    temp = getTemp()
    t2 = semantic_stack.pop()
    t1 = semantic_stack.pop()
    semantic_stack.append(temp)
    ThreeCodeAddress(ACTION.ADD, getParameter(t1), getParameter(t2), str(temp))


def sub():
    temp = getTemp()
    t2 = semantic_stack.pop()
    t1 = semantic_stack.pop()
    semantic_stack.append(temp)
    ThreeCodeAddress(ACTION.SUB, getParameter(t1), getParameter(t2), str(temp))


def mult():
    temp = getTemp()
    t1 = semantic_stack.pop()
    t2 = semantic_stack.pop()
    semantic_stack.append(temp)
    ThreeCodeAddress(ACTION.MULT, getParameter(t1), getParameter(t2), str(temp))


def lessThan():
    temp = getTemp()
    t2 = semantic_stack.pop()
    t1 = semantic_stack.pop()
    semantic_stack.append(temp)
    ThreeCodeAddress(ACTION.LT, getParameter(t1), getParameter(t2), str(temp))


def equal():
    temp = getTemp()
    t2 = semantic_stack.pop()
    t1 = semantic_stack.pop()
    semantic_stack.append(temp)
    ThreeCodeAddress(ACTION.EQ, getParameter(t1), getParameter(t2), str(temp))


def jumpOnFalse():
    # (JPF, A, L, )
    result = semantic_stack.pop()
    head = semantic_stack.pop()
    ThreeCodeAddress(ACTION.JPF, result, head)
    # jump destination and the result of expression are on top of stack.


def save():
    global pb_pointer
    semantic_stack.append(pb_pointer)
    ThreeCodeAddress(ACTION.JPF)


def jpf_save():
    global pb_pointer
    head = semantic_stack.pop()
    result = semantic_stack.pop()
    three_code_address_list[head].action = ACTION.JPF
    three_code_address_list[head].num1 = result
    three_code_address_list[head].num2 = (pb_pointer + 1)
    save()


def jp_save():  # jumps to the last saved spot
    global pb_pointer
    head = semantic_stack.pop()
    three_code_address_list[head]= ThreeCodeAddress(ACTION.JP, pb_pointer)
    three_code_address_list.pop()


def label():
    global pb_pointer
    semantic_stack.append(pb_pointer)


def jump_and_make_gap():
    global pb_pointer
    dest = pb_pointer + 2
    ThreeCodeAddress(ACTION.JP, dest)
    semantic_stack.append(str(pb_pointer) + "!")
    ThreeCodeAddress(ACTION.JPF)
    label()


def jump_for_break():
    if len(semantic_stack) < 2:
        semantic_check(SEMANTIC_ACTION.BREAK)
    else:
        stat = False
        for i in range(1, len(semantic_stack)):
            r = semantic_stack.copy()
            r.reverse()
            if type(r[i]) == str:
               if r[i][-1] == "!":
                    ThreeCodeAddress(ACTION.JP, int(r[i][0:-1]))
                    stat = True
                    break
        if not stat:        
            semantic_check(SEMANTIC_ACTION.BREAK)
       

def jump_until():
    global pb_pointer
    result = semantic_stack.pop()
    head = semantic_stack.pop()
    ThreeCodeAddress(ACTION.JPF, result, head)
    head = int(semantic_stack.pop()[0:-1])
    three_code_address_list[head].action = ACTION.JP
    three_code_address_list[head].num1 = pb_pointer


def funDeclare():
    global pb_pointer, scopeNumber
    semantic_stack.append(pb_pointer)
    ThreeCodeAddress(ACTION.JP)
    setFirstLine(previousToken.lexeme, len(three_code_address_list))
    scopeNumber += 1


def write_three_code_address():
    global three_code_address_list
    file = open("output.txt", "w")
    if len(three_code_address_list) != 0:
        for i in range(len(three_code_address_list)):
            if i == len(three_code_address_list) - 1:
                file.write(str(i) + "\t" + str(three_code_address_list[i]))
            else:
                file.write(str(i) + "\t" + str(three_code_address_list[i]) + "\n")
    else:
        file.write("")
    file.close()


# ########## Parser ########## #
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
    global lookahead, currentState, previousToken
    if terminal == "$":
        Node("$", parent)
    elif ((terminal == Token_Type.ID or terminal == Token_Type.NUM) and lookahead.type == terminal) or lookahead.lexeme == terminal:
        if lookahead.lexeme == "$":
            if terminal != "$":
                Syntax_Error(Syntax_Error_Type.UNEXPECTED_EOF)
            else:
                Node("$", parent)
        else:
            Node(str(lookahead), parent)
            previousToken = lookahead
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
    if lookahead.lexeme in first("Declaration-list"):  # Program -> #BYTE Declaration-list
        currentState = "Program"
        rootNode = Node(currentState)
        code_gen(ACTION.BYTE)
        declaration_list(rootNode)
    elif "EPSILON" in first("Declaration-list") and (
            lookahead.lexeme in follow_set["Program"] or lookahead.type.value in follow_set["Program"]):
        node = Node(state, parent)
        Node("epsilon", rootNode)
    elif checkError("Program"):
        program()


def declaration_list(parent_node):
    global lookahead, currentState
    # Declaration-list -> Declaration Declaration-list
    if lookahead.lexeme in first("Declaration Declaration-list"):
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
    # Declaration -> Declaration-initial Declaration-prime
    if lookahead.lexeme in first("Declaration-initial Declaration-prime"):
        currentState = "Declaration"
        node = Node(currentState, parent_node)
        declaration_initial(node)
        declaration_prime(node)
    elif checkError("Declaration"):
        declaration(parent_node)


def declaration_initial(parent_node):
    global lookahead, currentState
    # Declaration-initial -> Type-specifier #PUSHID ID
    if lookahead.lexeme in first("Type-specifier"):
        currentState = "Declaration-initial"
        node = Node(currentState, parent_node)
        type_specifier(node)
        code_gen(ACTION.PUSHID)
        match(Token_Type.ID, node)
    elif checkError("Declaration-initial"):
        declaration_initial(parent_node)


def type_specifier(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "int":  # Type-specifier -> #PUSHID int
        currentState = "Type-specifier"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match("int", node)
    elif lookahead.lexeme == "void":  # Type-specifier -> #PUSHID void
        currentState = "Type-specifier"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match("void", node)
    elif checkError("Type-specifier"):
        type_specifier(parent_node)


def declaration_prime(parent_node):
    global lookahead, currentState
    # Declaration-prime -> #MAINFUN Fun-declaration-prime
    if lookahead.lexeme in first("Fun-declaration-prime"):
        currentState = "Declaration-prime"
        node = Node(currentState, parent_node)
        code_gen(ACTION.MAINFUN)
        fun_declaration_prime(node)
    # Declaration-prime -> Var_declaration_prime #VARTYPE
    elif lookahead.lexeme in first("Var-declaration-prime"):
        currentState = "Declaration-prime"
        node = Node(currentState, parent_node)
        var_declaration_prime(node)
        semantic_check(SEMANTIC_ACTION.VARTYPE)
    elif checkError("Declaration-prime"):
        declaration_prime(parent_node)


def fun_declaration_prime(parent_node):
    global lookahead, currentState, isAnyFunDeclared
    if lookahead.lexeme == "(":  # Fun-declaration-prime -> ( Params ) Compound-stmt
        isAnyFunDeclared = True
        code_gen(ACTION.FUNDECLARE)
        currentState = "Fun-declaration-prime"
        node = Node(currentState, parent_node)
        match("(", node)
        code_gen(ACTION.GOTO_SAVE_AREA)
        params(node)
        match(")", node)
        compound_stmt(node)
    elif checkError("Fun-declaration-prime"):
        fun_declaration_prime(parent_node)


def var_declaration_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ";":  # Var-declaration-prime -> ; #INITIALIZE
        currentState = "Var-declaration-prime"
        node = Node(currentState, parent_node)
        match(";", node)
        code_gen(ACTION.INITIALIZE)
    elif lookahead.lexeme == "[":  # Var-declaration-prime -> [ #PUSHID NUM ] ; #ARRAY
        currentState = "Var-declaration-prime"
        node = Node(currentState, parent_node)
        match("[", node)
        code_gen(ACTION.PUSHID)
        match(Token_Type.NUM, node)
        match("]", node)
        match(";", node)
        code_gen(ACTION.ARRAY)
    elif checkError("Var-declaration-prime"):
        var_declaration_prime(parent_node)


def params(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "int":  # Params -> int #PUSHID ID Param-prime Param-list
        currentState = "Params"
        node = Node(currentState, parent_node)
        match("int", node)
        code_gen(ACTION.PUSHID)
        match(Token_Type.ID, node)
        param_prime(node)
        code_gen(ACTION.INITIALIZE)
        code_gen(ACTION.READ_VALUE)
        param_list(node)
    elif lookahead.lexeme == "void":  # Params -> void
        currentState = "Params"
        node = Node(currentState, parent_node)
        match("void", node)
    elif checkError("Params"):
        params(parent_node)


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
    if lookahead.lexeme in first("Statement Statement-list") or lookahead.type.value in first(
            "Statement Statement-list"):  # Statement-list -> Statement Statement-list
        currentState = "Statement-list"
        node = Node(currentState, parent_node)
        statement(node)
        statement_list(node)
    elif checkError("Statement-list", True, parent_node):
        statement_list(parent_node)


def expression_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first(
            "Expression"):  # Expression-stmt -> Expression ;
        currentState = "Expression-stmt"
        node = Node(currentState, parent_node)
        expression(node)
        match(";", node)
        # semantic_stack.pop()
    elif lookahead.lexeme == "break":  # Expression-stmt -> break ;
        currentState = "Expression-stmt"
        node = Node(currentState, parent_node)
        code_gen(ACTION.JPBREAK)
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
        code_gen(ACTION.SAVE)  # save
        statement(node)
        match("else", node)
        code_gen(ACTION.JPFSAVE)  # jump then save
        statement(node)
        code_gen(ACTION.JPSAVE)  # jump
    elif checkError("Selection-stmt"):
        selection_stmt(parent_node)


def iteration_stmt(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "repeat":  # Iteration-stmt -> repeat Statement until ( Expression )
        currentState = "Iteration-stmt"
        node = Node(currentState, parent_node)
        match("repeat", node)
        code_gen(ACTION.JPMAKEGAP)
        statement(node)
        match("until", node)
        match("(", node)
        expression(node)
        match(")", node)
        code_gen(ACTION.JPFUNTIL)
    elif checkError("Iteration-stmt"):
        iteration_stmt(parent_node)


def return_stmt_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression") or lookahead.type.value in first(
            "Expression"):  # Return-stmt-prime -> Expression ;
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
    if lookahead.lexeme in first("Expression-stmt") or lookahead.type.value in first(
            "Expression-stmt"):  # Statement -> Expression_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        expression_stmt(node)
    elif lookahead.lexeme in first("Compound-stmt") or lookahead.type.value in first(
            "Compound-stmt"):  # Statement -> Compound_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        compound_stmt(node)
    elif lookahead.lexeme in first("Selection-stmt") or lookahead.type.value in first(
            "Selection-stmt"):  # Statement -> Selection_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        selection_stmt(node)
    elif lookahead.lexeme in first("Iteration-stmt") or lookahead.type.value in first(
            "Iteration-stmt"):  # Statement -> Iteration_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        iteration_stmt(node)
    elif lookahead.lexeme in first("Return-stmt") or lookahead.type.value in first(
            "Return-stmt"):  # Statement -> Return_stmt
        currentState = "Statement"
        node = Node(currentState, parent_node)
        return_stmt(node)
    elif checkError("Statement"):
        statement(parent_node)


def simple_expression_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Additive-expression-zegond C") or lookahead.type.value in first(
            "Additive-expression-zegond C"):  # Simple-expression-zegond -> Additive-expression-zegond C
        currentState = "Simple-expression-zegond"
        node = Node(currentState, parent_node)
        additive_expression_zegond(node)
        c(node)
    elif checkError("Simple-expression-zegond"):
        simple_expression_zegond(parent_node)


def additive_expression_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term-zegond D") or lookahead.type.value in first(
            "Term-zegond D"):  # Additive-expression-zegond -> Term-zegond D
        currentState = "Additive-expression-zegond"
        node = Node(currentState, parent_node)
        term_zegond(node)
        d(node)
    elif checkError("Additive-expression-zegond"):
        additive_expression_zegond(parent_node)


def expression(parent_node): #debug
    global lookahead, currentState
    if lookahead.lexeme in first("Simple-expression-zegond") or lookahead.type.value in first(
            "Simple-expression-zegond"):  # Expression -> Simple_expression_zegond
        currentState = "Expression"
        node = Node(currentState, parent_node)
        simple_expression_zegond(node)
    elif lookahead.type == Token_Type.ID:  # Expression -> #PUSHID ID B
        currentState = "Expression"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        semantic_check(SEMANTIC_ACTION.SCOPING)
        match(Token_Type.ID, node)
        b(node)
    elif checkError("Expression"):
        expression(parent_node)


def c(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Relop Additive-expression") or lookahead.type.value in first(
            "Relop Additive-expression"):  # C -> Relop Additive-expression #RELOP
        currentState = "C"
        node = Node("C", parent_node)
        relop(node)
        additive_expression(node)
        code_gen(ACTION.RELOP)
    elif checkError("C", True, parent_node):
        c(parent_node)


def relop(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "<":  # Relop -> #PUSHID <
        currentState = "Relop"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match("<", node)
    elif lookahead.lexeme == "==":  # Relop -> #PUSHID ==
        currentState = "Relop"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match("==", node)
    elif checkError("Relop"):
        relop(parent_node)


def addop(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "+":  # Addop -> #PUSHID +
        currentState = "Addop"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match("+", node)
    elif lookahead.lexeme == "-":  # Addop -> #PUSHID -
        currentState = "Addop"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match("-", node)
    elif checkError("Addop"):
        addop(parent_node)


def d(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Addop Term D") or lookahead.type.value in first(
            "Addop Term D"):  # D -> Addop Term #EXPRESSION D
        currentState = "D"
        node = Node(currentState, parent_node)
        addop(node)
        term(node)
        code_gen(ACTION.EXPRESSION)
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
    if lookahead.lexeme == "*":  # G -> #PUSHID * Factor #EXPRESSION G
        currentState = "G"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match("*", node)
        factor(node)
        code_gen(ACTION.EXPRESSION)
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
    elif lookahead.type == Token_Type.ID:  # Factor -> #PUSHID #SCOPING ID Var-call-prime
        currentState = "Factor"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        semantic_check(SEMANTIC_ACTION.SCOPING)
        match(Token_Type.ID, node)
        var_call_prime(node)
    elif lookahead.type == Token_Type.NUM:  # Factor -> #PUSHID NUM
        currentState = "Factor"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match(Token_Type.NUM, node)
    elif checkError("Factor"):
        factor(parent_node)


def arg_list(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Expression Arg-list-prime") or lookahead.type.value in first(
            "Expression Arg-list-prime"):  # Arg-list -> Expression Arg-list-prime
        currentState = "Arg-list"
        node = Node(currentState, parent_node)
        code_gen(ACTION.ALLOCATE_SAVE_AREA)
        expression(node)
        code_gen(ACTION.SAVE_ARG)
        arg_list_prime(node)
    elif checkError("Arg-list"):
        arg_list(parent_node)


def args(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Arg-list") or lookahead.type.value in first("Arg-list"):  # Args -> Arg-list
        currentState = "Args"
        node = Node(currentState, parent_node)
        arg_list(node)
        code_gen(ACTION.SAVE_RETURN_AND_JUMP)
    elif checkError("Args", True, parent_node):
        args(parent_node)


def arg_list_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == ",":  # Arg-list-prime -> , Expression Arg-list-prime
        currentState = "Arg-list-prime"
        node = Node(currentState, parent_node)
        match(",", node)
        expression(node)
        code_gen(ACTION.SAVE_ARG)
        arg_list_prime(node)
    elif checkError("Arg-list-prime", True, parent_node):
        arg_list_prime(parent_node)


def term_zegond(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Factor-zegond G") or lookahead.type.value in first(
            "Factor-zegond G"):  # Term-zegond -> Factor-zegond G
        currentState = "Term-zegond"
        node = Node(currentState, parent_node)
        factor_zegond(node)
        g(node)
    elif checkError("Term-zegond"):
        term_zegond(parent_node)


def factor_zegond(parent_node): #debug
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor-zegond -> ( Expression )
        currentState = "Factor-zegond"
        node = Node(currentState, parent_node)
        match("(", node)
        expression(node)
        match(")", node)
    elif lookahead.type == Token_Type.NUM:  # Factor-zegond -> #PUSHID NUM
        currentState = "Factor-zegond"
        node = Node(currentState, parent_node)
        code_gen(ACTION.PUSHID)
        match(Token_Type.NUM, node)
    elif checkError("Factor-zegond"):
        factor_zegond(parent_node)


def b(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "=":  # B -> = Expression #ASSIGN
        currentState = "B"
        node = Node(currentState, parent_node)
        match("=", node)
        expression(node)
        code_gen(ACTION.ASSIGN)
    elif lookahead.lexeme == "[":  # B -> [ Expression ] #SETADDRESS H
        currentState = "B"
        node = Node(currentState, parent_node)
        match("[", node)
        expression(node)
        match("]", node)
        code_gen(ACTION.SETADDRESS)
        h(node)
    elif lookahead.lexeme in first("Simple-expression-prime") or lookahead.type.value in first(
            "Simple-expression-prime"):  # B -> Simple-expression-prime
        currentState = "B"
        node = Node(currentState, parent_node)
        simple_expression_prime(node)
    elif checkError("B"):
        b(parent_node)


def h(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "=":  # H -> = Expression #ASSIGN
        currentState = "H"
        node = Node(currentState, parent_node)
        match("=", node)
        expression(node)
        code_gen(ACTION.ASSIGN)
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
    if lookahead.lexeme == "[":  # Var-prime -> [ Expression ] #SETADDRESS
        currentState = "Var-prime"
        node = Node(currentState, parent_node)
        match("[", node)
        expression(node)
        match("]", node)
        code_gen(ACTION.SETADDRESS)
    elif checkError("Var-prime", True, parent_node):
        var_prime(parent_node)


def simple_expression_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Additive-expression-prime C") or lookahead.type.value in first(
            "Additive-expression-prime C"):  # Simple-expression-prime -> Additive-expression-prime C
        currentState = "Simple-expression-prime"
        node = Node(currentState, parent_node)
        additive_expression_prime(node)
        c(node)
    elif checkError("Simple-expression-prime"):
        simple_expression_prime(parent_node)


def additive_expression_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Term-prime D") or lookahead.type.value in first(
            "Term-prime D"):  # Additive-expression-prime -> Term-prime D
        currentState = "Additive-expression-prime"
        node = Node(currentState, parent_node)
        term_prime(node)
        d(node)
    elif checkError("Additive-expression-prime"):
        additive_expression_prime(parent_node)


def term_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme in first("Factor-prime G") or lookahead.type.value in first(
            "Factor-prime G"):  # Term-prime -> Factor-prime G
        currentState = "Term-prime"
        node = Node(currentState, parent_node)
        factor_prime(node)
        g(node)
    elif checkError("Term-prime"):
        term_prime(parent_node)


def factor_prime(parent_node):
    global lookahead, currentState
    if lookahead.lexeme == "(":  # Factor-prime -> ( Args #PRINT )
        currentState = "Factor-prime"
        node = Node(currentState, parent_node)
        match("(", node)
        args(node)
        match(")", node)
        code_gen(ACTION.PRINT)
    elif checkError("Factor-prime", True, parent_node):
        factor_prime(parent_node)


def write_parse_tree():
    global rootNode

    file = open("parse_tree.txt", "w", encoding="utf-8")
    for pre, _, node in RenderTree(rootNode):
        file.write(("%s%s" % (pre, node.name)) + "\n")
    file.close()


# ########## Scanner ########## #
class Token_Type(Enum):
    NUM = "NUM"
    ID = "ID"
    KEYWORD = "KEYWORD"
    SYMBOL = "SYMBOL"
    COMMENT = "COMMENT"
    WHITESPACE = "WHITESPACE"
    FINAL = "FINAL"


class Token:
    def __init__(self, lexeme="", type=Token_Type.ID, line=0, needToAddToTokenList=True):
        self.lexeme = lexeme
        self.type = type
        self.line = line
        self.address = 0
        self.varType = ""
        self.numberOfArgument = None
        self.argList = []
        self.returnVal = None
        self.scope = 0
        self.firstLine = None
        if (type == Token_Type.ID or type == Token_Type.KEYWORD) and lexeme not in symbol_table:
            symbol_table.append(self)
        if needToAddToTokenList and self not in token_list:
            token_list.append(self)

    def __str__(self):
        return "(" + self.type.name + ", " + self.lexeme + ")"


def setTempForToken(lexeme, temp):
    for t in symbol_table:
        if t.lexeme == lexeme:
            t.address = temp


def getTempOfToken(lexeme):
    for t in symbol_table:
        if t.lexeme == lexeme:
            return t.address


def setVarTypeForToken(lexeme, type):
    for t in symbol_table:
        if t.lexeme == lexeme:
            t.varType = type


def getVarTypeOfToken(lexeme):
    for t in symbol_table:
        if t.lexeme == lexeme:
            return t.varType


def setScope(lexeme, scope):
    for t in symbol_table:
        if t.lexeme == lexeme:
            t.scope = scope


def getScope(lexeme):
    for t in symbol_table:
        if t.lexeme == lexeme:
            return t.scope


def setFirstLine(lexeme, lineNo):
    for t in symbol_table:
        if t.lexeme == lexeme:
            t.firstLine = lineNo


def getFirstLine(lexeme):
    for t in symbol_table:
        if t.lexeme == lexeme:
            return t.firstLine


def addParameterToFun(lexeme, param):
    for t in symbol_table:
        if t.lexeme == lexeme:
            t.argList.append(param)


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

    if TokenType != Token_Type.COMMENT and TokenType != Token_Type.WHITESPACE and TokenType is not None:
        out_put = Token(lexeme, TokenType, lineno)
    else:
        out_put = get_next_token(input_file)

    return out_put


def findType(token):
    if token in keywords:
        return Token_Type.KEYWORD
    else:
        return Token_Type.ID


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


def initial_error_writer():
    file = open("lexical_errors.txt", "w")
    file.write("There is no lexical error.")
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


main()
