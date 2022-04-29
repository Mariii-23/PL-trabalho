#!/usr/bin/env python3

from LL1 import LL1, Condiction, Exp
first_rule = ""

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
    string += "\ntokens = ("
    for token in ll1.tokens:
        string += token + ","
    string = string[:len(string)-1]
    string += ")\n\n"

    for token in ll1.tokens:
        regex = ll1.tokens[token]
        name = token[1:len(token)-1]
        string += "t_" + name + " = r" + regex +"\n"

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
    print("Erro sintático: ", simb)\n

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        value = prox_simb.value
        prox_simb = lexer.token()
        return value
    else:
        parserError(simb)\n
"""

def add_endParser():
    global string, first_rule
    string += """
def rec_Parser(data):
    print("Starting...")
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_""" + first_rule + """()
    print("That's the end.")

linha = input("Introduza: ")
rec_Parser(linha)
"""

def add_term(ll1:LL1, token):
    string = ""
    if token in ll1.literals or token in ll1.tokens:
        string += "\trec_term(" + token + ")\n"
    else:
        string += "\trec_" + token + "()\n"
    return string

def add_rules(ll1: LL1):
    global string, first_rule
    rules = ""
    for rule in ll1.rules:
        if len(first_rule) == 0:
            first_rule = rule

        rule_ = "def rec_" + rule + "():\n"+"\tglobal prox_simb\n"
        exp = ll1.exps[rule]
        # TODO como pode ter varios separar
        if len(exp.condictions) == 1:
            for token in exp.condictions[0].rules:
                rule_ += add_term(ll1, token)
        else:
            isFirst = True
            for condiction in exp.condictions:
                if isFirst:
                    isFirst = False
                    # todo talvez falte saber se é rule, se for tenho q ir buscar o locahed
                    rule_+= "\tif prox_simb.type in ["
                    for elem in condiction.symbols:
                        rule_ += elem + ","
                    rule_ = rule_[:len(rule_)-1]
                    rule_ += "]:\n"
                else:
                    rule_+= "\telif prox_simb.type in ("
                    for elem in condiction.symbols:
                        rule_ += elem + ","
                    rule_ = rule_[:len(rule_)-1]
                    rule_ += "):\n"
                if len(condiction.rules) == 0:
                    rule_ += "\t\tpass\n"
                for token in condiction.rules:
                    rule_ += "\t" +add_term(ll1, token)

            rule_ += "\telse:\n\t\tparserError(prox_simb)\n"
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
