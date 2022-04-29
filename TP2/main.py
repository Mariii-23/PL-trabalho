#!/usr/bin/env python3
from parserGramatica import parser_Gramatica
from LL1 import LL1, Condiction, Exp
from buildParser import buildParser

import sys
programa = sys.stdin.read()
LL1 = parser_Gramatica(programa)
# print(LL1)

# print("Is this a LL1??? -> ", LL1.isLL1())

stringFile = buildParser(LL1)
print(stringFile)
