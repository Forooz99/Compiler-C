from enum import Enum

# Alireza Foroodniya 99105645, Foroozan Iraji 99105272
digits = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}
symbols = {";", ":", "{", "}", "[", "]", "(", ")", "<", "+", "-", ","}
keywords = {"break", "else", "if", "int", "repeat", "return", "until", "void"}
symbol_table = []
token_list = []
characterBuffer = None
error_list = []
lineno = 1

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
    UNMATCHED_COMMNET = "Unmatched comment"
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
        return "("+ self.type.name + ", " + self.lexeme + ")"


class Error:
    def __init__(self , lexeme="", error_type=ERROR_Type , line=0):
        self.lexeme = lexeme
        self.type = error_type
        self.line = line
        error_list.append(self)

    def __str__(self) -> str:
        return "(" + self.lexeme + ", " + self.type.value + ")"
        

    

def main():
    # initialize keywords as first tokens & add to symbol_table
    for keyword in keywords:
        Token(keyword, Type.KEYWORD, needToAddToTokenList=False)

    input_file = open("input.txt", "r")

    #characterBuffer = input_file.read(1)

    while get_next_token(input_file):
        get_next_token(input_file)

    input_file.close()


    # for s in symbol_table:
    #     print(s)


    for i in token_list:
        print(i)

    for i in error_list:
        print(i)    

    #createOutputs()

    initial_error_writer()
    file_writer(token_list, "tokens.txt")
    file_writer(error_list , "lexical_errors.txt")
    symbol_writer()


def initial_error_writer():
    file = open("lexical_errors.txt", "w")
    file.write("There is no lexical error.")
    file.close()

def file_writer(content, file_name):
    if content:
        file = open(file_name,"w")
        string = str(content[0].line) + ".\t" + str(content[0]) + " "
        for i in range(1,len(content)):
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




# TODO: if file ends in * or = or digit code crashes

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
        elif state == 1 and (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122 or nextCharacter in digits):
            state = 1
            lexeme += nextCharacter
            nextCharacter = file.read(1)
        
        
        #matching ERROR inside IDs
        elif state == 1 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122 or nextCharacter in digits or nextCharacter in symbols) and not (nextCharacter.isspace()) and nextCharacter != "*" and nextCharacter != "/" and nextCharacter != "=":
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
        # elif state == 3 and ((nextCharacter in digits) or nextCharacter.isspace() or (nextCharacter in symbols)) and nextCharacter != "*" and nextCharacter != "/" :
        #     state = 100
        #     TokenType = Type.NUM
        #     characterBuffer = nextCharacter
        
        # matching NUM ERRORS
        elif state == 3 and not(nextCharacter in digits) and not nextCharacter.isspace() and not(nextCharacter in symbols) and nextCharacter != "=" and nextCharacter != "*" and nextCharacter != "/" :
            state = 4
            lexeme += nextCharacter
        elif state == 4:
            state = 100
            Error(lexeme, ERROR_Type.INVALID_NUMBER, lineno)
        elif state == 3:
            state = 100
            TokenType = Type.NUM
            characterBuffer = nextCharacter
        
        # elif state == 4 and not nextCharacter.isspace() and not(nextCharacter in symbols):
        #     state = 4
        #     lexeme += nextCharacter
        #     nextCharacter = file.read(1)
        # elif state == 4 and (nextCharacter.isspace() or (nextCharacter in symbols)):
        #     state = 100
        #     characterBuffer = nextCharacter
        #     Error(lexeme, ERROR_Type.INVALID_NUMBER, lineno)
 
        
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
        elif state == 5 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122 or nextCharacter in digits or nextCharacter in symbols) and not (nextCharacter.isspace()) and nextCharacter != "*" and nextCharacter != "/":
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
            
        # TODO: changes to be done to make \ illegeal character    
        elif state == 11 and nextCharacter != "*":
            state = 16

        elif state == 12 and nextCharacter == "":
            Error("/*" + lexeme[0:5] + "...", ERROR_Type.UNCLOSED_COMMENT, lineno)
            return 0
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
            Error(lexeme, ERROR_Type.UNMATCHED_COMMNET, lineno)
        elif state == 14 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122 or nextCharacter in digits or nextCharacter in symbols) and not (nextCharacter.isspace()) and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 14 and nextCharacter != "/":
            state = 7
            characterBuffer = nextCharacter


        # this state was used when incorrect nextCharacter is encountered 
        # I read next char because in case of
        # "/" it must be read
        elif state == 0:
            lexeme += nextCharacter
            nextCharacter = file.read(1)
            state = 15
        elif state == 15:
            state = 100
            characterBuffer = nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno) 
        elif state == 16 and not (65 <= ord(nextCharacter) <= 90 or 97 <= ord(nextCharacter) <= 122 or nextCharacter in digits or nextCharacter in symbols) and not (nextCharacter.isspace()) and nextCharacter != "/":
            state = 100
            lexeme += nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)
        elif state == 16:
            state = 100
            characterBuffer = nextCharacter
            Error(lexeme, ERROR_Type.INVALID_INPUT, lineno)


        

    if lexeme == "\n":
        lineno += 1
    if TokenType != Type.COMMENT and TokenType != Type.WHITESPACE and TokenType != None:
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
