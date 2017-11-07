#!/usr/bin/env python
# @Author  : pengyun

# 解析输入

import string
from buffer import Buffer
from expr import *

SYMBOL_STARTS = set(string.ascii_lowercase + string.ascii_uppercase + '_')
SYMBOL_INNERS = SYMBOL_STARTS | set(string.digits)
NUMERAL = set(string.digits + '-.')
WHITESPACE = set(' \t\n\r')
DELIMITERS = set('(),:')

def is_literal(s):
    return isinstance(s, (int, float))

def is_name(s):
    return isinstance(s, str) and s not in DELIMITERS and s != 'lambda'

# tokenize

def tokenize(s):
    """
     >>> tokenize('lambda f: f(0, 4.2)')
    ['lambda', 'f', ':', 'f', '(', 0, ',', 4.2, ')']
    :param s:
    :return:
    """
    src = Buffer(s)
    tokens = []
    while True:
        token = next_token(src)
        if token is None:
            return tokens
        tokens.append(token)

def take(src, allow_char):
    """根据具体的规则获取具体的字符"""
    result = ''
    while src.current() in allow_char:
        result += src.pop()
    return result

def next_token(src):
    """获取一个token"""
    take(src, WHITESPACE)
    c = src.current()
    if c is None:
        return c
    elif c in NUMERAL:
        literal = take(src, NUMERAL)
        try:
            return int(literal)
        except ValueError:
            try:
                return float(literal)
            except ValueError:
                raise SyntaxError("{} is not a numeral".format(literal))
    elif c in SYMBOL_STARTS:
        return take(src, SYMBOL_INNERS)
    elif c in DELIMITERS:
        src.pop()
        return c
    else:
        raise SyntaxError("{} is not a token".format(c))


def read(s):
    src = Buffer(tokenize(s))
    if src.current() is not None:
        return read_expr(src)

def read_expr(src):
    """将经过tokenize 分割的字符转化为具体的对象"""
    token = src.pop()
    if token is None:
        raise SyntaxError('Incomplete expression')
    elif is_literal(token):
        return read_call_expr(src, Literal(token))
    elif is_name(token):
        return read_call_expr(src, Name(token))
    elif token == 'lambda':
        params = read_comma_separated(src, read_param)
        src.expect(':')
        body = read_expr(src)
        return LambdaExpr(params, body)
    elif token == '(':
        inner_expr = read_expr(src)
        src.expect(')')
        return read_call_expr(src, inner_expr)
    else:
        raise SyntaxError("{} is not the start of a expression".format(token))

def read_comma_separated(src, reader):
    if src.current() in (':', ')'):
        return []
    else:
        s = [reader(src)]
        while src.current() == ',':
            src.pop()
            s.append(reader(src))
        return s

def read_call_expr(src, operator):
    while src.current() == '(':
        src.pop()
        operands = read_comma_separated(src, read_expr)
        src.expect(')')
        operator = CallExpr(operator, operands)
    return operator

def read_param(src):
    token = src.pop()
    if is_name(token):
        return token
    else:
        raise SyntaxError("Expected parameter name but got '{}'".format(token))


