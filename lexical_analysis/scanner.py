import new_tokenizer
from Token import *

# Alireza Foroodniya 99105645, Foroozan Iraji 99105272

# token type: NUM / ID / KEYWORD / SYMBOL / COMMENT / WHITESPACE
# list for each type except comment, whitespace(these will be ignored):


# class Type(Enum):
#     KEYWORD = 1
#     ID = 2
#     NUM = 3
#     SYMBOL = 4
#     COMMENT = 5
#     WHITESPACE = 6



def main():
    symbol_count = 1
    file = open("input.txt", "r")
    symbol_file = open("symbol_table.txt", "w")
    token_file = open("tokens.txt", "w")

    tokenizer = new_tokenizer.Tokenizer(file)
    
    while tokenizer.get_next_token() != 0 :
        tokenizer.get_next_token()

    # completing symbol table file
    for i in symbol_table:
        symbol_file.write(str(symbol_count) + ".\t" + i + "\n")
        symbol_count += 1


    
    # completing token table file
    for list in token_list:
        add_line = False
        string = ""

        for token in list:
            if token.type != Type.COMMENT and token.type != Type.WHITESPACE:
                add_line = True

        if add_line:
            string += str(list[0].line + 1) + ".\t"
            for token in list:
                if token.type != Type.COMMENT and token.type != Type.WHITESPACE: 
                    string += str(token) + " "

        if string != "":
            string += "\n"
            token_file.write(string)

                
        







main()
