#!/usr/bin/env python3

class Condiction:
    def __init__(self, tokens: list = [], symbols = [], last_symbol: str = ''):
        self.tokens =  tokens
        self.symbols = symbols
        self.last_symbol = last_symbol

    def __str__(self):
        phrase = ""
        for value in self.tokens:
            phrase += value + " "
        phrase += "\t\t{ "
        for value in self.symbols :
            phrase += value + " "
        phrase += "}"
        return phrase

    # def insert(self, token, symbols = []):
    #     self.tokens += [token]
    #     if len(self.symbols) == 0:
    #         self.symbols = symbols

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
        self.tokens = []
        self.literals = []

    def __str__(self):
        phrase = "Tokens : "
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

    def build_symbols_exp(self, name):
        if name not in self.exps:
            return []
        exp = self.exps[name]
        symbols = exp.symbols
        if len(symbols) == 0:
            exp = self.exps[name]
            if len(self.exps[exp.name].symbols) != 0:
                symbols = symbols
            else:
                for condiction in exp.condictions:
                    symbols += self.search_symbol(condiction, exp.name)
                # condiction.symbols = symbols
            self.exps[exp.name].symbols = symbols

        return symbols

    def get_last_symbols(self, name_exp):
       last_symbols = []
       exp = self.exps[name_exp]
       for condiction in exp.condictions:
           last = condiction.last_symbol
           if last in self.literals:
               last_symbols += [last]
           else:
               print(last)
               print(exp.name)
           # TODO nao tou a perceber porque raio
           # else:
               # if last not in self.exps:
               #     print("fds")
               # exp_aux = self.exps[last]
               # for condiction2 in exp_aux.condictions:
               #     if len(condiction2.symbols) > 0:
               #         last_symbols += [condiction2.symbols[-1]]
               #     else:
               #         last_symbols += self.build_symbols_right(last)

           #     last_symbols += self.get_last_symbols(last)
       return last_symbols

    def get_symbols_rigth(self, name):
       symbols = []
       exp = self.exps[name]
       for condiction in exp.condictions:
           value = condiction.last_symbol
           if value != '':
               if value in self.literals:
                   symbols += [value]
               else:
                   symbols += self.get_symbols_rigth(value)
           else:
               for name_ in self.exps:
                   exp_aux = self.exps[name_]
                   for condiction in exp.condictions:
                       last = ""
                       for token in condiction.tokens:
                           if name_ == last:
                               if last in self.literals:
                                   symbols += [token]
                               else:
                                   print(token_)
                                   symbols += self.get_last_symbols(token_)
                           last = token
               symbols += self.build_symbols_right(name)
       return symbols

    def build_symbols_right(self, name):
        symbols = []
        for exp in self.exps:
            exp = self.exps[exp]
            for condiction in exp.condictions:
                    last = ""
                    for token in condiction.tokens:
                        if token == name:
                            if last == "" :
                                symbols += self.get_symbols_rigth(exp.name)
                            elif last in self.literals:
                                symbols += [last]
                            else:
                                symbols += self.get_last_symbols(last)
                        last = token

        return symbols

    def search_symbol(self, condiction, exp_name):
        symbols = condiction.symbols
        if len(symbols) == 0:
            if len(condiction.tokens) > 0:
                value = condiction.tokens[0]
                symbols = self.build_symbols_exp(value)
            else:
                #procurar a direita
                # symbols = self.build_symbols_right(exp_name)
                print("fuck this")

            condiction.symbols = symbols
        return symbols

    def build_symbols_exps(self):
        for exp in self.exps:
            self.build_symbols_exp(exp)
    # TODO
    def isLL1(self):
        result = True
        for exp in self.exps:
            exp = self.exps[exp]
            if len(exp.condictions) == 1:
                continue
            values = set()
            for condiction in exp.condictions:
                if not result:
                    return result
                length = len(values)
                values.add(tuple(condiction.tokens))
                result = length < len(values)

        return result
