#!/usr/bin/env python
# @Author  : pengyun


# 一个简单的计算器，用来理解程序语言是如何执行的。
# calc>>3!
# 6
# calc>>+(2,3,4,5!)
# 129


from operator import add, mul, sub
from functools import reduce
from tools import main

# Input(text) >> Lexical analysis(token) >> Syntactic analysis(expression) >>


known_operators = {'add', 'sub', 'mul', 'div', '+', '-', '*', '/'}
fact = lambda x: 1 if x == 1 else fact(x-1)*x


def assert_non_token(tokens):
    if len(tokens) == 0:
        raise SyntaxError('Input Wrong')

# Parse

class Exp:
    """
    >>> Exp('add', [1, 2])
    Exp('add', [1, 2])
    >>> str(Exp('add', [1, Exp('mul', [2, 3])]))
    'add(1, mul(2, 3))'
    """
    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return 'Exp ({}, {})'.format(self.operator, self.operands)

    def __str__(self):
        operands = ', '.join(map(str, self.operands))
        return '({}  {})'.format(self.operator, operands)

def tokenize(line):
    """将输入拆成一个列表"""
    spaced = line.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ')
    return spaced.strip().split()

def analyze_operands(tokens):
    """将操作数拆出来，配合analyze 构造表达式树"""
    assert_non_token(tokens)
    operands = []
    while tokens[0] != ')':
        if operands and tokens.pop(0) != ',':
            raise SyntaxError('expected ,')
        operands.append(analyze(tokens))
        assert_non_token(tokens)
    tokens.pop(0) # remove )
    return operands

def analyze_token(token):
    """解析具体的token"""
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return token

def analyze(tokens):
    """构造表达式树"""
    assert_non_token(tokens)
    token = analyze_token(tokens.pop(0))
    if type(token) in (int, float):
        return token
    elif token[-1] == '!':
        return fact(int(token[:-1]))
    if token in known_operators:
        # 操作符号 后紧跟的是 （
        if len(tokens) == 0 or tokens.pop(0) != '(':
            raise SyntaxError('Excepted ( after ' + token)
        return Exp(token, analyze_operands(tokens))
    else:
        raise SyntaxError('unexpected ' + token)

def calc_parse(input):
    token = tokenize(input)
    expression_token = analyze(token)
    return expression_token

# eval
def calc_eval(exp):
    if type(exp) in (int, float):
        return exp
    elif isinstance(exp, Exp):
        argument = list(map(calc_eval, exp.operands))
        return calc_apply(exp.operator, argument)
    else:
        raise TypeError


def calc_apply(op, argument):
    if op in ('+', 'add'):
        return sum(argument)
    elif op in ('-', 'sub'):
        if len(argument) == 0:
            raise TypeError(op + 'must have one argument')
        elif len(argument) == 1:
            return -argument
        else:
            return sum(argument[:1] + [-i for i in argument[1:]])
    elif op in ('*', 'mul'):
        return reduce(mul, argument, 1)
    elif op in ('/', 'div'):
        if len(argument) != 2:
            raise TypeError(op + 'must have two argument')
        numer, denom = argument
        return numer / denom

# read_eval_loop 好多语言都可以交互式的执行。
# 打印提示 1
# 读取用户输入 2
# 解析输入 3
# 执行解析后的输入 4
# 捕获错误，返回 5
# 返回结果 6

@main
def read_eval_loop():
    while True:
        try:
            expression = calc_parse(input('calc>>')) # 1，2，3
            print(calc_eval(expression)) # 4， 6
        except (SyntaxError, TypeError, ZeroDivisionError) as e: # 5
            print(type(e).__name__ + ':', e)
        except(KeyboardInterrupt, EOFError):
            # ctrl D -- exit
            print("Bye ~~~")
            return


