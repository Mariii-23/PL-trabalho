#!/usr/bin/env python3

from LL1 import LL1, Condiction, Exp
first_rule = ""

string = """
#!/usr/bin/env python3

import ply.lex as lex
import ply.yacc as yacc
"""

def add_literals(ll1: LL1):
    global string
    string += "\nliterals = ["
    for literal in ll1.literals:
       string += literal + ","
    string = string[:len(string)-1]
    string += "]\n"

def add_tokens(ll1: LL1):
    global string
    string += "\ntokens = ["
    for token in ll1.tokens:
        string += token + ","
    string = string[:len(string)-1]
    string += "]\n\n"

    for token in ll1.tokens:
        regex = ll1.tokens[token]
        name = token[1:len(token)-1]
        string += "def t_" + name + "(t):\n"
        string += "\tr" + regex +"\n"
        # TODO aqui podemos devolver outra cena
        string += "\treturn t\n"


def add_lexer():
    global string
    string += """
def t_new_line(t):
    r'\\n+'
    t.lexer.lineno += len(t.value)

t_ignore = "\\t "

def t_error(t):
    print("Erro léxico no token '%s" %  t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()\n
"""


def add_term(exp: Exp, ll1: LL1):
    global string
    i = 0

    for condiction in exp.condictions:
        string += "def p_" + exp.name +"_" + str(i) + "(p):\n\t"
        string +="\"" + exp.name + " : "
        for elem in condiction.rules:
            if elem in ll1.tokens:
                elem = elem[1:len(elem)-1]
            string += elem + " "
        string = string[:len(string)-1]
        string +="\"\n\n"
        i+=1
        # TODO depois aqui podemos por acoes


def add_rules(ll1: LL1):
    global first_rule
    for exp in ll1.exps :
        if len(first_rule) == 0:
            first_rule = exp
        add_term(ll1.exps[exp],ll1)

def add_endParser():
    global string, first_rule
    string += """def p_error(p):
    print("Erro sintatico:, ",p)
    parser.success = False

# Build the parser
parser = yacc.yacc()
parser.success = True

# Read line from input and parse it
import sys
for linha in sys.stdin:
    parser.success = True
    parser.parse(linha)
    if parser.success:
        print("Success")
    else:
        print("Error")
"""

def buildParser(ll1: LL1):
    global string
    add_literals(ll1)
    add_tokens(ll1)
    add_lexer()
    add_rules(ll1)
    add_endParser()
    return string
