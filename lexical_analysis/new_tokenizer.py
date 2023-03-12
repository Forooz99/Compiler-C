from Token import *



digit = {"0","1","2","3","4","5","6","7","8","9"}
symbols = {";",":","{","}","[","]","(",")","<"}




class Tokenizer:
    def __init__(self, file):
        self.file = file
        self.Character_buffer = None
        self.line = 0


    def findType(self,input):
        if input == "if" or input == "else" or input == "void" or input == "int" or input == "repeat" or input == "break" or input == "until" or input == "return":
            return Type.KEYWORD
        else:
            return Type.ID

    
    def get_next_token(self):
        state = 0
        token_found = False
        TokenType = None
        lexeme = ""
        j = 0 
        line = None

        #TODO : handle end of file if its digit or Identifier

        if self.Character_buffer:
                input = self.Character_buffer
                self.Character_buffer = None
        else:
                input = self.file.read(1)
        
        #TODO : be more completed
        if not input:
            return 0
            
        while state != 100:
            


            # matching ID and Keywords's Using State 1 & 2
            if state == 0 and ((ord(input) >= 65 and ord(input) <= 90) or (ord(input) >= 97 and ord(input) <= 122)): #re.search("[a-zA-Z]", input)
            
                state = 1
                lexeme += input
                input = self.file.read(1)

            elif state == 1 and ((ord(input) >= 65 and ord(input) <= 90) or (ord(input) >= 97 and ord(input) <= 122) or input in digit): #re.search("[a-zA-Z0-9]", input)
                state = 1
                lexeme += input
                input = self.file.read(1)
                

            elif state == 1 :
                state = 100
                self.Character_buffer = input
                TokenType = self.findType(lexeme)


            # matching NUM's Using State 3 & 4
            elif state == 0 and input in digit:
                state = 3
                lexeme += input
                input = self.file.read(1)


            elif state == 3 and input in digit:
                state = 3
                lexeme += input
                input = self.file.read(1)
                


            elif state == 3:
                state = 100
                TokenType = Type.NUM
                self.Character_buffer = input




            # matching SYMBOL using state 5 & 6 & 7
            elif state == 0 and input in symbols:
                state = 7
                lexeme += input



            elif state == 0 and input == "=":
                state = 5
                lexeme += input
                input = self.file.read(1)
                


            elif state == 5 and input == "=":
                state = 100
                lexeme += input
                TokenType = Type.SYMBOL

                
            
            elif state == 5:
                state = 100
                TokenType = Type.SYMBOL
                self.Character_buffer = input


            elif state == 7:
                state = 100
                TokenType = Type.SYMBOL



            # matching WHITESPACE using state 8 & 9 & 10
            elif state == 0 and input.isspace():
                lexeme += input
                state = 8


            elif state == 8:
                state = 100
                TokenType = Type.WHITESPACE






            # matching comments using states starting from 11
            elif state == 0 and input == "/":
                input = self.file.read(1)
                state = 11


            elif state == 11 and input == "*":
                input = self.file.read(1)
                state = 12


            elif state == 12 and input != "*":
                lexeme += input
                input = self.file.read(1)
                state = 12


            elif state == 12 and input == "*":
                lexeme += input
                input = self.file.read(1)
                state = 13


            elif state == 13 and input != "/":
                lexeme += input
                input = self.file.read(1)
                state = 12

                
            elif state == 13 and input == "/":
                lexeme = lexeme.rstrip(lexeme[-1])
                TokenType = Type.COMMENT
                state = 100

            
            # this state was used when incorrect input is given
            elif state == 0:
                state = 100
    



        
        if lexeme == "\n" :
            self.line += 1

        new_token = Token(lexeme, TokenType,token_list,self.line)
        
        if lexeme not in symbol_table and TokenType != Type.WHITESPACE and TokenType != Type.COMMENT:
            symbol_table.append(lexeme)
            
        
        return 1





