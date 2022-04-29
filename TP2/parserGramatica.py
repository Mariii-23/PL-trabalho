#!/usr/bin/env python3
import ply.lex as lex
tokens = ('ID', 'SETA', 'END', 'SEP', 'END_PARSER', 'LITERAL', 'ATOKENS',
          'FCLOSE', 'ALITERALS', 'REGEX', 'EQUALS')

t_EQUALS = '='
t_ID = r'[A-Za-z]\w*'
t_LITERAL = r'\'[^\']+\''
t_SETA = r'->'
t_END = r';'
t_END_PARSER = r'.'
t_SEP = r'\|'

t_FCLOSE = r'\s*\]'
t_ALITERALS = r'Literals\s*=\s*\[\s*'

t_ATOKENS = r'Tokens\s*=\s*\[\s*'

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
    exit(-1)

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

def rec_Tokens(tokens: list = [], symbols: list = [], last: str = ''):
    global prox_simb, LL1
    if prox_simb == None:
        parserErrorExit()
    if prox_simb.type == 'ID':
        value = rec_term('ID')
        acoes = rec_Tokens(tokens + [value], symbols, value)
        tokens = acoes.rules
        symbols = acoes.symbols
        last = acoes.last_symbol
    elif prox_simb.type == 'LITERAL':
        value = rec_term('LITERAL')
        if value not in LL1.literals and  value not in LL1.tokens :
            parserError(prox_simb)
            print("Token or Id dont exist: " + value)
            exit(-1)

        symbols = [value] if len(symbols) == 0 else symbols
        acoes = rec_Tokens(tokens + [value], symbols, value)
        tokens = acoes.rules
        symbols = acoes.symbols
        last = acoes.last_symbol
    elif prox_simb.type == 'END':
        rec_term('END')
    else:
        parserError(prox_simb)
    return Condiction(tokens, symbols, last)

def rec_Condicao():
    value = ""
    symbols = []
    if prox_simb == None:
        parserErrorExit()
    if prox_simb.type == 'ID':
        value = rec_term('ID')
    elif prox_simb.type == 'LITERAL':
        value = rec_term('LITERAL')
        # LL1.literals += [value]
        symbols = [value]
    else:
        parserError(prox_simb)

    return rec_Tokens([value], symbols, value)

def rec_Condicoes():
    global prox_simb
    if prox_simb == None:
        parserErrorExit()
    condicoes = []
    if prox_simb.type == 'SEP':
        rec_term('SEP')
        condicao = rec_Tokens()
        condicoes = [condicao]
        condicoes += rec_Condicoes()
    elif prox_simb.type == 'END':
        rec_term('END')
    else:
        parserError(prox_simb)
    return condicoes

def rec_Exp():
    global prox_simb
    global LL1
    name = rec_term('ID')
    LL1.rules += [name]

    rec_term('SETA')

    condicao = rec_Condicao()
    condicoes = [condicao]
    condicoes += rec_Condicoes()
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

def rec_Gramatica():
    global LL1
    exp = rec_Exp()
    LL1.insert(exp)
    rec_Exps()

def rec_ListTokens():
    global prox_simb
    global LL1
    if prox_simb == None:
        parserErrorExit()

    dist = {}
    if prox_simb.type == 'LITERAL':
        name = rec_term('LITERAL')
        rec_term('EQUALS')
        regex = rec_term('LITERAL')
        dist[name] = regex

        listResto = rec_ListTokens()
        dist.update(listResto)

    return dist

def rec_ValidsTOKENS():
    rec_term('ATOKENS')
    tokens = rec_ListTokens()
    rec_term('FCLOSE')
    return tokens

def rec_ListLiterals():
    global prox_simb
    global LL1
    if prox_simb == None:
        parserErrorExit()
    list = []
    if prox_simb.type == 'LITERAL':
        name = rec_term('LITERAL')
        list = [name] + rec_ListLiterals()

    return list

def rec_ValidsLiterals():
    rec_term('ALITERALS')
    tokens = rec_ListLiterals()
    rec_term('FCLOSE')
    return tokens


def rec_Start():
    global LL1
    LL1.literals =  rec_ValidsLiterals()
    LL1.tokens = rec_ValidsTOKENS()
    rec_Gramatica()

def rec_Parser(data):
    global prox_simb
    lexer.input(data)
    prox_simb = lexer.token()
    rec_Start()
    # print("Gramática correta")
    # print("\nEstrutura lida ate agora: \n")

def parser_Gramatica(programa):
    global LL1
    # print("\nStarting...")
    rec_Parser(programa)
    LL1.build_symbols_exps()
    return LL1
