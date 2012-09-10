import itertools, math, operator as op, re

stack = [0,0,0,0,0]
variables = []
values = []
varstack = []

def enter(number):
    global stack
    number = float(number)
    stack = list(itertools.chain([number],stack[0:4]))

def compute(operator):
    global stack
    if operator not in funcarg1:
        res = functions[operator](stack[1],stack[0])
        stack = list(itertools.chain([res],stack[2:5],[0]))
    else:
        res = functions[operator](stack[0])
        stack[0] = res
    print "["+str(stack[0])+"]"

def assign(number):
    global varstack
    global variables
    global values
    try:
        var = varstack.pop()
    except IndexError:
        print "no variable to assign"
        return
    if var in variables:
        values[variables.index(var)] = number
    else:
        variables.append(var)
        values.append(number)
    return number

functions = {"+":op.add, "-":op.sub, "*":op.mul, "/":op.div,
             "**":op.pow, "//":op.floordiv, "%":op.mod, "#": lambda m,e:m**(1/e),
             "&":op.and_, "|":op.or_, "^":op.xor, "~":op.inv,
             "abs":op.abs, "neg":op.neg, "ceil":math.ceil, "floor":math.floor,
             "sin":math.sin, "sinh":math.sinh, "asin":math.asin, "asinh":math.asinh,
             "cos":math.cos, "cosh":math.cosh, "acos":math.acos, "acosh":math.acosh,
             "tan":math.tan, "tanh":math.tanh, "atan":math.atan, "atanh":math.atanh,
             "hypot":math.hypot, "frexp":math.frexp, "ldexp":math.ldexp, "log":math.log,
             "rad":math.radians, "deg":math.degrees, "fac":math.factorial,
             "=":assign}
funcarg1 = ["~","abs","neg","ceil","floor","sin","sinh","asin","asinh",
            "cos","cosh","acos","acosh","tan","tanh","atan","atanh","frexp",
            "ldexp","rad","deg","fac","="]

def tokenizer(inp):
    tokens = inp.split(" ")
    number_re = re.compile(r"""[0-9]*\.?[0-9]+""")
    symbol_re = re.compile(r"""\$?\w+""")
    alltokens = []
    alltokentypes = []
    for token in tokens:
        if number_re.match(token) != None:
            alltokens.append(number_re.match(token).group())
            alltokentypes.append(0)
        elif symbol_re.match(token) != None:
            alltokens.append(symbol_re.match(token).group())
            alltokentypes.append(1)
        elif token in ["=","*","+","-","/","&","%","|","^","~","**","//","#"]:
            alltokens.append(token)
            alltokentypes.append(2)
        else:
            print "unknown expression."
    return alltokens, alltokentypes

def parse(inp):
    global varstack
    alltokens, alltokentypes = tokenizer(inp)
    for i in range(len(alltokens)):
        token = alltokens[i]
        tType = alltokentypes[i]
        if tType == 0:
            enter(float(token))
        elif tType == 2:
            compute(token)
        elif tType == 1:
            if token[0] == "$":
                if token in variables:
                    varstack.insert(0,token)
                    enter(values[variables.index(token)])
                    print "["+str(values[variables.index(token)])+"]"
                elif token not in variables:
                    varstack.insert(0,token)
            else:
                parse(token)

if __name__ == "__main__":
    print "Zwiebel 0.01"
    while True:
        try:
            inp = raw_input(":>")
            parse(inp)
        except EOFError:
            break
