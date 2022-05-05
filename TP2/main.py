#!/usr/bin/env python3
from parserGrammar import parser_Grammar
from LL1 import LL1, Condiction, Exp
from buildParser import buildParser

import sys
programa = sys.stdin.read()
LL1 = parser_Grammar(programa)
# print(LL1)

# print("Is this a LL1??? -> ", LL1.isLL1())
if LL1.isLL1():
    stringFile = buildParser(LL1)
    print(stringFile)
else:
    print("The grammar isn't a LL1 parser\n")
