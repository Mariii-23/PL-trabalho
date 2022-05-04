#!/usr/bin/env python3
#
import numpy as np

class Condiction:
    def __init__(self, tokens: list = [], symbols: list = [], last_symbol: str = ''):
        self.rules =  tokens
        self.symbols = symbols
        self.last_symbol = last_symbol

    def __str__(self):
        phrase = ""
        for value in self.rules:
            phrase += value + " "
        phrase += "\t\t{ "
        for value in self.symbols :
            phrase += value + " "
        phrase += "}"
        return phrase

class Exp:
    def __init__(self, name, condictions):
        self.name = name
        self.condictions =  condictions
        self.symbols = []

    def __str__(self):
        phrase = self.name + " -> "
        first = True
        for condiction in list(self.condictions):
            if first:
                first = False
            else:
                phrase +=  "     | "
            phrase += condiction.__str__() + " "
            phrase += "\n"

        # phrase += "\t{ "
        # for symbol in self.symbols:
        #     phrase += symbol + " "
        # phrase += "}\n"
        return phrase

class LL1:
    def __init__(self, exps = {}):
        self.exps = exps
        self.rules = []
        self.tokens = {}
        self.literals = []

    def __str__(self):
        phrase = "Rules : "
        for token in self.rules:
            phrase += token + " "
        phrase += "\nTokens : "
        for token in self.tokens:
            phrase += token + " "
        phrase += "\nLiterals : "
        for literal in self.literals:
            phrase += literal + " "
        phrase += "\n\n"
        for exp in self.exps:
            phrase += self.exps[exp].__str__()
            phrase += "\n"

        return phrase

    def insert(self, exp: Exp):
        self.exps[exp.name] = exp

    def build_symbols_exp(self, name, dont_look=[]):
        if name not in self.exps or name in dont_look:
            return []
        exp = self.exps[name]
        symbols = exp.symbols
        if len(symbols) == 0:
            for condiction in exp.condictions:
                    symbols += self.search_symbol(condiction, exp.name, dont_look + [name])
            self.exps[exp.name].symbols = symbols

        return symbols

    def get_follow_symbols(self, name_exp, dont_look):
       symbols = []
       exp = self.exps[name_exp]
       for condiction in exp.condictions:
           if len(condiction.rules) == 0:
               symbols += self.build_symbols_right(exp.name, [])
           else:
               symbols_condiction = condiction.symbols
               if len(symbols_condiction) == 0:
                   symbols_condicton = self.build_symbols_right(exp.name, [])
               symbols += symbols_condiction
       return symbols


    def build_symbols_right(self, name, dont_look):
        symbols = []
        for exp in self.exps:
            exp = self.exps[exp]
            if exp.name == name or exp.name in dont_look:
                continue
            for condiction in exp.condictions:
                length = len(condiction.rules)
                if name in condiction.rules:
                    rules = np.array(condiction.rules)
                    indexs = np.where(rules == name)[0]

                    for index in indexs:
                        if length-1 == index:
                            symbols += self.build_symbols_right(exp.name, dont_look+[name])
                        else:
                            elem_name =  condiction.rules[index + 1]
                            if elem_name in self.literals:
                                symbols += [elem_name]
                            else:
                                symbols += self.get_follow_symbols(elem_name, [])
        return symbols

    def search_symbol(self, condiction, exp_name, dont_look = []):
        symbols = condiction.symbols
        if len(symbols) == 0:
            if len(condiction.rules) > 0:
                value = condiction.rules[0]
                symbols = self.build_symbols_exp(value, dont_look)
            else:
                #procurar a direita
                symbols = self.build_symbols_right(exp_name, [] + exp_name)

            condiction.symbols = symbols
        return symbols

    def build_symbols_exps(self):
        for exp in self.exps:
            self.build_symbols_exp(exp)

    def isLL1(self):
        result = True
        if len(self.tokens) == 0 and len(self.literals) == 0:
            return False
        for exp in self.exps:
            exp = self.exps[exp]
            # if len(exp.condictions) == 1:
            #     continue
            values = []
            for condiction in exp.condictions:
                if not result:
                    return result
                if len(condiction.symbols) == 0:
                    return False

                for value in condiction.symbols:
                    if value in values:
                        result = False
                    else:
                        values += [value]
        return result
