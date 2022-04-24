#!/usr/bin/env python3
import ply.lex as lex
tokens = ('ID', 'SETA', 'END', 'SEP', 'END_PARSER', 'LITERAL')

t_ID = r'[A-Za-z]\w*'
t_LITERAL = r'\'[^\']+\''
t_SETA = r'->'
t_END = r';'
t_END_PARSER = r'.'
t_SEP = r'\|'

# define a rule so we can track line numbers
def t_new_line(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore = "\t "

def t_error(t):
    print("Erro léxico no token '%s" %  t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()
####
####

from LL1 import LL1, Condiction, Exp
LL1 = LL1()
prox_simb = ('Erro', '',0,0)

# TODO escrever um erro melhor
def parserError(simb):
    print("Erro sintático: ", simb)

def parserErrorExit():
    print("Erro sintático")
    print("Gramática Incorreta")
    exit(-1)

def rec_term(simb):
    global prox_simb
    if prox_simb.type == simb:
        value = prox_simb.value
        prox_simb = lexer.token()
        return value
    else:
        parserError(simb)
        exit(-1)

def rec_Tokens(acoes: list):
    global prox_simb
    if prox_simb == None:
        parserErrorExit()
    if prox_simb.type == 'ID':
        value = rec_term('ID')
        acoes = rec_Acoes(acoes + [value])
    elif prox_simb.type == 'LITERAL':
        value = rec_term('LITERAL')
        acoes = rec_Acoes(acoes + [value])
    elif prox_simb.type == 'END':
        rec_term('END')
    else:
        parserError(prox_simb)
    return acoes

def rec_Condicao():
    value = ""
    symbols = []
    if prox_simb == None:
        parserErrorExit()
    if prox_simb.type == 'ID':
        value = rec_term('ID')
    elif prox_simb.type == 'LITERAL':
        value = rec_term('LITERAL')
        LL1.literals += [value]
        symbols = [value]
    else:
        parserError(prox_simb)

    condicao = Condiction(rec_Tokens([value]), symbols)

def rec_Condicoes(condicoes):
    global prox_simb
    if prox_simb == None:
        parserErrorExit()
    if prox_simb.type == 'SEP':
        rec_term('SEP')
        rec_Condicao()
        condicoes = rec_Condicoes(condicoes + [condicao])
    elif prox_simb.type == 'END':
        rec_term('END')
    else:
        parserError(prox_simb)
    return condicoes

def rec_Exp():
    global prox_simb
    global LL1
    name = rec_term('ID')
    LL1.tokens += [name]

    rec_term('SETA')

    rec_Condicao()
    condicoes = rec_Condicoes([condicao])
    return Exp(name,condicoes)


def rec_Exps():
    global prox_simb
    global LL1
    if prox_simb == None:
        parserErrorExit()
    if prox_simb.type == 'ID':
        exp = rec_Exp()
        LL1.insert(exp)
        rec_Exps()
    elif prox_simb.type == 'END_PARSER':
        rec_term('END_PARSER')
    else:
        parserError(prox_simb)

def rec_Start():
    rec_Exps()

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Start()
    print("Gramática correta")
    print("\nEstrutura lida ate agora: \n")

def parser_Gramatica(programa):
    global LL1
    print("\nStarting...")
    rec_Parser(programa)
    # LL1.build_symbols()
    return LL1