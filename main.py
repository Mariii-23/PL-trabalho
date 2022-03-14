import re, sys
from dataclasses import dataclass


data = []

def parse_header(header):
    for field in header:
        rng = r"\{\d+(,\d+)?\}"
        if re.search(rng, field):
            if re.search(rng+"::\w+"):
                # range with associate function

        else:
            # normal  ou invalido se tiver tipo um {


keys = sys.stdin.readline().split(',')
for line in sys.stdin:
    print(line)
