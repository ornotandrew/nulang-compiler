import ply.yacc as yacc
import sys
from lex import tokens
from exceptions import *


class Node:

    def __init__(self, val=None, child=[]):
        self.value = val
        self.children = child


def print_node(N, depth=0):
    if type(N) == Node:
        print("\t" * depth, N.value, sep="")
        for child in N.children:
            print_node(child, depth + 1)
    else:
        print("\t" * depth, N, sep="")


def p_program(p):
    """ Program : Statement_Closure """
    p[0] = Node("Program", p[1])


def p_statement_closure(p):
    """ Statement_Closure : Statement_Closure Statement """
    p[0] = p[1] + [p[2]]


def p_statement_closure_epsilon(p):
    """ Statement_Closure : """
    p[0] = []


def p_statement(p):
    """ Statement : ID EQUALS Expression """
    varname = p[1]
    if varname in varnames:
        raise SemanticException(p.lineno(1), varname, True)
    else:
        varnames.append(varname)
        p[0] = Node("AssignStatement", ["ID," + str(varname), p[3]])


def p_expression_plus(p):
    """ Expression : Expression PLUS Term """
    p[0] = Node("AddExpression", [p[1], p[3]])


def p_expression_minus(p):
    """ Expression : Expression MINUS Term """
    p[0] = Node("SubExpression", [p[1], p[3]])


def p_expression_term(p):
    """ Expression : Term """
    p[0] = p[1]


def p_term_times(p):
    """ Term : Term TIMES Factor """
    p[0] = Node("MulExpression", [p[1], p[3]])


def p_term_divide(p):
    """ Term : Term DIVIDE Factor """
    p[0] = Node("DivExpression", [p[1], p[3]])


def p_term_factor(p):
    """ Term : Factor """
    p[0] = p[1]


def p_factor_lparen(p):
    """ Factor : LPAREN Expression RPAREN """
    p[0] = p[2]


def p_factor_float(p):
    """ Factor : FLOAT_LITERAL """
    p[0] = Node("FloatExpression", ["FLOAT_LITERAL," + str(p[1])])


def p_factor_id(p):
    """ Factor : ID """
    varname = p[1]
    if not varname in varnames:
        raise SemanticException(p.lineno(1), varname, False)
    else:
        p[0] = Node("IdentifierExpression", ["ID," + str(varname)])


# Error rule for syntax errors
def p_error(p):
    raise ParserException(p.lineno, p)


# Build the parser
parser = yacc.yacc(debug=0)

# Keep track of definitions
varnames = []


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        try:
            root = Node("Start", [parser.parse(f.read())])
        except Exception as e:
            print(e)
            sys.exit()

    # Traverse the tree
    print_node(root)
