import new_tokenizer
from Token import *

# Alireza Foroodniya 99105645, Foroozan Iraji 99105272




def main():
    symbol_count = 1
    file = open("input.txt", "r")
    symbol_file = open("symbol_table.txt", "w")
    token_file = open("tokens.txt", "w")
    error_file = open("lexical_errors.txt","w")

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


    error_file.write("There is no lexical error.")

    # for list in token_list:
    #     for token in list:
    #         if token.type != Type.WHITESPACE:
    #             print(token)                
        







main()
