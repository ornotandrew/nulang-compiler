import ply.yacc as yacc
import sys

# Get the token map from the lexer.  This is required.
from lex import tokens


class Node:

    def __init__(self, val=None, child=[]):
        self.value = val
        self.children = child


def print_node(N, depth):
    if type(N) == Node:
        # This caters for Kleene Closure cases where we don't want to print out the intermediate productions
        if N.value is None: 
            depth-=1
        else:
            print("\t" * depth, N.value, sep="")
        for child in N.children:
            print_node(child, depth + 1)
    else:
        print("\t" * depth, N, sep="")



def p_program(p):
    """ Program : Functiondecl_Closure Statement_Closure """
    p[0] = Node("Program", [p[1], p[2]])


def p_functiondecl_closure(p):
    """ Functiondecl_Closure : Functiondecl_Closure Functiondecl """
    p[0] = Node(None, [p[1], p[2]]) 


def p_functiondecl_closure_epsilon(p):
    """ Functiondecl_Closure : """
    p[0] = Node(None, [])


def p_functiondecl(p):
    """ Functiondecl : FunctionHead FunctionBody """
    p[0] = Node("Functiondecl", [p[1], p[2]])


def p_functionhead(p):
    """ FunctionHead : FUNC ID LPAREN ID RPAREN """
    p[0] = Node("Functionhead", ["FUNC", "ID,"+str(p[2]), "(", "ID,"+str(p[4]), ")"])

def p_functionbody(p):
    """ FunctionBody : LBRAC Statement_Closure RBRAC """
    p[0] = Node("Functionbody", ["{", p[2], "}"])


def p_statement_closure(p):
    """ Statement_Closure : Statement_Closure Statement """
    p[0] = Node(None, [p[1], p[2]])


def p_statement_closure_epsilon(p):
    """ Statement_Closure : """
    p[0] = Node(None, [])


def p_statement(p):
    """ Statement : ID EQUALS Expression """
    p[0] = Node("Statement", ["ID,"+str(p[1]), "=", p[3]])


def p_expression_plus(p):
    """ Expression : Expression PLUS Term """
    p[0] = Node("CaseplusExpression", [p[1], "+", p[3]])


def p_expression_minus(p):
    """ Expression : Expression MINUS Term """
    p[0] = Node("CaseminusExpression", [p[1], "-", p[3]])


def p_expression_term(p):
    """ Expression : Term """
    p[0] = Node("CasetermExpression", [p[1]])


def p_term_times(p):
    """ Term : Term TIMES Factor """
    p[0] = Node("CasemultiplyTerm", [p[1], "*", p[3]])


def p_term_divide(p):
    """ Term : Term DIVIDE Factor """
    p[0] = Node("CasedivideTerm", [p[1], "/", p[3]])


def p_term_factor(p):
    """ Term : Factor """
    p[0] = Node("CasefactorTerm", [p[1]])


def p_factor_lparen(p):
    """ Factor : LPAREN Expression RPAREN """
    p[0] = Node("CasebracsFactor", ["(", p[2], ")"])


def p_factor_idlparen(p):
    """ Factor : ID LPAREN Expression RPAREN """
    p[0] = Node("CasefuncFactor", ["ID,"+str(p[1]), "(", p[3], ")"])


def p_factor_float(p):
    """ Factor : FLOAT_LITERAL """
    p[0] = Node("CasefloatFactor", ["FLOAT_LITERAL,"+str(p[1])])


def p_factor_id(p):
    """ Factor : ID """
    p[0] = Node("CaseidFactor", ["ID,"+str(p[1])])


# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc(debug=0)


if __name__ == "__main__":
    with open(sys.argv[1]) as f:
        try:
            root = Node("Start", [parser.parse(f.read())])
        except:
            print(locals())

    # Traverse the tree
    print_node(root, 0)
