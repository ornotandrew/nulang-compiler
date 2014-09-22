import ply.lex as lex
import sys
from exceptions import LexerException

# List of token names.
reserved = {"func": "FUNC"}

tokens = [
    "ID",
    "FLOAT_LITERAL",
    "PLUS",
    "MINUS",
    "TIMES",
    "DIVIDE",
    "EQUALS",
    "WHITESPACE",
    "COMMENT",
    "LPAREN",
    "RPAREN",
    "LBRAC",
    "RBRAC",
] + list(reserved.values())


# Regular expression rules for simple tokens
t_FLOAT_LITERAL = r'[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'\/'
t_EQUALS = r'='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRAC = r'\{'
t_RBRAC = r'\}'


def t_ID(t):
    r'([A-Za-z]|_)(\w|_|)*'
    t.type = reserved.get(t.value, 'ID')    # Check for reserved words
    return t


def t_WHITESPACE(t):
    r'\s+'
    inc_lineno(t)
    if __name__ == "__main__":
        return t
    else:
        pass


def t_COMMENT(t):
    r'\/\*[\s\S]*\*\/|\/\/.*'
    inc_lineno(t)
    if __name__ == "__main__":
        return t
    else:
        pass


def inc_lineno(t):
    '''Guard to make sure line numbers are correct'''
    t.lexer.lineno += t.value.count("\n")


# Error handling rule
def t_error(t):
    raise LexerException(t.lineno, t)
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


if __name__ == "__main__":
        # Give the file data to the lexer
    with open(sys.argv[1]) as f:
        lexer.input(f.read())

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        typ = tok.type
        val = tok.value

        if typ in ["ID", "FLOAT_LITERAL"]:
            print(typ, ",", val, sep="")
        elif typ in ["FUNC", "WHITESPACE", "COMMENT"]:
            print(typ)
        elif typ in ["PLUS", "MINUS", "TIMES", "DIVIDE", "EQUALS",
                             "LPAREN", "RPAREN", "LBRAC", "RBRAC"]:
            print(val)
