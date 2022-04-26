#!/usr/bin/env python3

from LL1 import LL1, Condiction, Exp

string = """
#!/usr/bin/env python3

import ply.lex as lex
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

lexer = lex.lex()
####
prox_simb = ('Erro', '',0,0)

def parserError(simb):
    print("Erro sintático: ", simb)
"""

def add_endParser():
    global string
    string += """
def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Calc()
    print("That's the end...")

linha = input("Introduza: ")
rec_Parser(linha)
"""

def add_rules(ll1: LL1):
    global string
    rules = ""
    for rule in ll1.rules:
        rule_ = "def rec_" + rule + "():\n"
        # print(rule)
        exp = ll1.exps[rule]
        # TODO como pode ter varios separar
        for condiction in exp.condictions:
            for token in condiction.rules:
                if token in ll1.literals:
                    rule_ += "\trec_term(" + token + ")\n"
                else:
                    rule_ += "\trec_" + token + "()\n"
        rules_back = rules
        rules = rule_ + "\n"
        rules += rules_back
    string += rules

def buildParser(ll1: LL1):
    global string
    add_literals(ll1)
    add_tokens(ll1)
    add_lexer()

    add_rules(ll1)

    add_endParser()

    return string
