import sys, re

class Field:
    def __init__(self, name, minimum = 1, maximum = 1, agg_fun = lambda x:x):
        self.name = name
        self.min =  minimum
        self.max = maximum
        self.agg_fun = agg_fun

    def __str__(self):
         return "name: %s , min: %s, max: %s, agg_fun: %s" % (self.name,
                 self.min, self.max , self.agg_fun.__name__)


fields = []
#new_field = Field("names", 0, 10, lambda l : ' '.join(l))
str_regex = r'[a-zA-Z_]+[\w/]*'
rng_regex = "(\w+){(\d+)(?:,(\d+))?}"

token_specification = [
        ('AGG_FUNCTION', r'(%s|%s)(::(\w+))' % (str_regex, rng_regex)),
        ('RANGE', rng_regex),
        ('STR', str_regex),
]

tok_regex = '|'.join(('(?P<%s>%s)') % pair for pair in token_specification)


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
    else:
        if dic['AGG_FUNCTION']:
            r = dic['AGG_FUNCTION'].split('::')
            fun = eval(r[1])
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

    print(field)
    fields.append(field)

def parse_header():
    r = re.finditer(tok_regex, sys.stdin.readline())
    for i in r:
            dic = i.groupdict()
            create_field(dic)

def csv_to_json():
    return

parse_header()
csv_to_json()
