#!/usr/bin/env python3
import re
from enum import Enum
import argparse
import sys

class Type(Enum):
    VAR = 0
    ARRAY = 1
    OP = 2

class Field:
    def __init__(self, name, minimum = 1, maximum = 1, agg_fun = lambda x:x, type_field = Type.VAR):
        self.name = name
        self.min =  int(minimum)
        self.max = int(maximum)
        self.agg_fun = agg_fun
        self.type = type_field

    def __str__(self):
         return "name: %s , min: %s, max: %s, agg_fun: %s, type: %s" % (self.name,
                                                                        self.min, self.max , self.agg_fun.__name__, self.type)
fields = []
min = 0
max = 0
result = "["



def media(l):
    return sum(l) /len(l)

# recebe nome{...}
def parse_range(line):
    r = re.search(rng_regex, line)
    maybe_max = r.group(3)
    minimum = r.group(2)
    maximum = maybe_max if maybe_max else minimum
    return {"name": r.group(1), "min": minimum, "max": maximum}

def create_field(dic):
    field = None
    fun = None
    minimum = maximum = 1
    if dic['STR']:
        field = Field(dic['STR'])
        field.type = Type.VAR
    else:
        if dic['AGG_FUNCTION']:
            r = dic['AGG_FUNCTION'].split('::')
            try:
                fun = eval(r[1])
            except NameError:
                print("Aggregation Function Does Not Exist...")
                return
            # se tiver um range {x,y} ou {x}
            dict_range = parse_range(r[0])
        elif dic['RANGE']:
            dict_range = parse_range(dic['RANGE'])

        if (dict_range):
            minimum = dict_range['min']
            maximum = dict_range['max']
            field = Field(dict_range['name'], minimum, maximum)

        if(fun):
            field.agg_fun = fun
            field.type = Type.OP
        else:
            field.type = Type.ARRAY
    # print(field)
    fields.append(field)
    global min, max
    min += field.min
    max += field.max

def parse_header(line):
    r = re.finditer(tok_regex, line)
    for i in r:
            dic = i.groupdict()
            create_field(dic)

def parse_Field(line,minimo, maximo):
    global result
    global r
    line = line[:-1]
    list_words = r.findall(line)
    if len(list_words) - 1 < minimo or len(list_words) -1 > maximo:
        return
    indice = 0

    result += f'\n{" "*4}'
    result += '{'
    for elem in fields:
        if elem.type == Type.OP:
            array = []
            for _ in range(elem.max):
                num = list_words[indice]
                if num != "":
                    array.append(int(num))
                indice += 1
            result += f'\n{" "*8}\"{elem.name}_{elem.agg_fun.__name__}\": '
            value = elem.agg_fun(array)
            result += f'{value}{separator}'

        elif elem.type == Type.ARRAY:
            array = []
            for _ in range(elem.max):
                num = list_words[indice]
                if num != "":
                    array.append(int(num))
                indice += 1
            result += f'\n{" "*8}\"{elem.name}\": {array}{separator}'
        else:
            result += f'\n{" "*8}\"{elem.name}\": \"{list_words[indice]}\"{separator}'
            indice += 1
    result = result[:len(result)-1]
    result += f'\n{" "*4}'
    result += "}" + separator

def csv_to_json(f):
    global result
    for line in f.readlines():
        parse_Field(line, min, max)
    if(len(result) > 1):
        result = result[:len(result)-1]
    result += "\n]"

parser = argparse.ArgumentParser(description='CSV TO JSON')

parser.add_argument('input_file')
parser.add_argument('output_file')
parser.add_argument('-F')
args = parser.parse_args()
inputfile = args.input_file
separator = ',' if not args.F else args.F
outputfile = re.search('[^\.]+', inputfile).group(0) + ".json" if len(sys.argv) == 2 else sys.argv[2]

str_regex = r'[a-zA-Z_]+[^'+separator+r'\n]*'
rng_regex = r"(\w+){(\d+)(?:,(\d+))?}"

token_specification = [
        ('AGG_FUNCTION', r'(%s|%s)(::(\w+))' % (str_regex, rng_regex)),
        ('RANGE', rng_regex),
        ('STR', str_regex),
]

tok_regex = '|'.join(('(?P<%s>%s)') % pair for pair in token_specification)

f = open(inputfile, "r")
r = re.compile(r'([^'+separator+'\n]*)'+separator+'?')

parse_header(f.readline())
csv_to_json(f)

out = open(outputfile, "w")
out.write(result)
out.close()
