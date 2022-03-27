#!/usr/bin/env python3
import re
from enum import Enum
import argparse
import sys

class Field:
    def __init__(self, name, minimum = 1, maximum = 1, agg_fun = lambda x:x):
        self.name = name
        self.min =  int(minimum)
        self.max = int(maximum)
        self.agg_fun = agg_fun

    def __str__(self):
         return "name: %s , min: %s, max: %s, agg_fun: %s" % (self.name,
                                                                        self.min, self.max , self.agg_fun.__name__)
fields = []
min = 0
max = 0
result = "["

def media(l):
    return sum(l) /len(l)

def hello(l):
    return "Hello::" + l + "::Hello"

# recebe nome{...}
def parse_range(line):
    r = re.search(rng_regex, line)
    if r:
        maybe_max = r.group(3)
        minimum = r.group(2)
        maximum = maybe_max if maybe_max else minimum
        name = r.group(1)
    else:
        minimum = 1
        maximum = 1
        name = line
    return {"name": name, "min": minimum, "max": maximum}

def create_field(dic):
    field = None
    fun = None
    minimum = maximum = 1
    global r_split, r

    if dic['STR']:
        field = Field(dic['STR'])
    else:
        if dic['AGG_FUNCTION']:
            r_ = r_split.search(dic['AGG_FUNCTION'])
            try:
                fun = eval(r_.group(2))
            except NameError:
                print("Aggregation Function Does Not Exist...")
                return
            # se tiver um range {x,y} ou {x}
            field = Field(r_.group(1))
            dict_range = parse_range(r_.group(1))
            if (dict_range):
                minimum = dict_range['min']
                maximum = dict_range['max']
                field = Field(dict_range['name'], minimum, maximum)

        elif dic['RANGE']:
            dict_range = parse_range(dic['RANGE'])

            if (dict_range):
                minimum = dict_range['min']
                maximum = dict_range['max']
                field = Field(dict_range['name'], minimum, maximum)
        else:
            list_words = r.findall(dic['ERROR'])
            print("Error found in header: " + list_words[1])
            exit(1)

        if(fun):
            field.agg_fun = fun
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

    try:
        result += f'\n{" "*4}'
        result += '{'
        for elem in fields:
            result += f'\n{" "*8}\"{elem.name}'
            if elem.agg_fun.__name__ == "<lambda>":
                result += '\": '
            else:
                result += f'_{elem.agg_fun.__name__}\": '
            if elem.max == 1:
                value = list_words[indice]
                indice += 1
                if elem.agg_fun.__name__ == "<lambda>":
                    result += f'\"{value}\"'
                else:
                    result += f'{elem.agg_fun(value)}'
            else:
                array = []
                for _ in range(elem.max):
                    num = list_words[indice]
                    if num != "":
                        array.append(num)
                    indice += 1

                if elem.agg_fun.__name__ == "<lambda>":
                    result += '['
                    for elem in array:
                        result += f'\"{elem}\",'
                    result = result[:len(result)-1]
                    result += ']'
                else:
                    array = [int(num, base=16) for num in array]
                    result += f'{elem.agg_fun(array)}'
            result+= ","
        result = result[:len(result)-1]
        result += f'\n{" "*4}'
        result += "},"
    except Exception:
        result += "},"
        return

def csv_to_json(f):
    global result
    for line in f.readlines():
        parse_Field(line, min, max)
    if(len(result) > 1):
        result = result[:len(result)-1]
        result += "\n"
    result += "]"

parser = argparse.ArgumentParser(description='CSV TO JSON')

# parser.add_argument('input_file')
# parser.add_argument('output_file')
parser.add_argument('-F')
args = parser.parse_args()
# inputfile = args.input_file
separator = ',' if not args.F else args.F
# outputfile = re.search('[^\.]+', inputfile).group(0) + ".json" if len(sys.argv) == 2 else sys.argv[2]

str_regex = r'[a-zA-Z_]+[^'+separator+r'\n]*'
rng_regex = r"(\w+){(\d+)(?:,(\d+))?}"

token_specification = [
        ('AGG_FUNCTION', r'(%s|%s)(::(\w+))' % (str_regex, rng_regex)),
        ('RANGE', rng_regex),
        ('STR', str_regex),
]

tok_regex = '|'.join(('(?P<%s>%s)') % pair for pair in token_specification)

# f = open(inputfile, "r")
f = sys.stdin
r = re.compile(r'([^'+separator+'\n]*)'+separator+'?')
r_split = re.compile(r'(\w+(?:{\d+(?:,\d+)?})?)::(.+)')

parse_header(f.readline())
# for field in fields:
#     print(field)
csv_to_json(f)

print(result)
# out = open(outputfile, "w")
# out.write(result)
# out.close()
