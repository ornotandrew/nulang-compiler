import sys

class LexerException(Exception):

    def __init__(self, line, token):
        self.line = line
        self.col = find_column(token)
        self.token = token.value[0]

    def __str__(self):
        return "nulang.lexer.LexerException: [{0},{1}] Unknown token: {2}".format(self.line, self.col, self.token[0])


class ParserException(Exception):

    def __init__(self, line, token):
        self.line = line
        self.col = find_column(token)

    def __str__(self):
        return "nulang.parser.ParserException: [{0},{1}] expecting: EOF".format(self.line, self.col)


class SemanticException(Exception):

    def __init__(self, line, varname, isdef):
        self.line = line
        self.varname = varname
        self.isdef = isdef

    def __str__(self):
        if self.isdef:
            return "SemanticException: [{0}] {1} already defined.".format(self.line, self.varname)
        else:
            return "SemanticException: [{0}] {1} not defined.".format(self.line, self.varname)


# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(token):
    with open(sys.argv[1]) as f:
        input = f.read()
        last_cr = input.rfind('\n', 0, token.lexpos)
        if last_cr < 0:
            last_cr = 0
            column = (token.lexpos - last_cr) + 1
        return column
