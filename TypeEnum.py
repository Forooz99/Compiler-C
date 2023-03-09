from enum import Enum


class Type(Enum):
    KEYWORD = 1
    ID = 2
    NUM = 3
    SYMBOL = 4
    COMMENT = 5
    WHITESPACE = 6