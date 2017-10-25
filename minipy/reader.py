#!/usr/bin/env python
# @Author  : pengyun

# 解析输入

import string
from buffer import Buffer

SYMBOL_STARTS = set(string.ascii_lowercase + string.ascii_uppercase + '_')
SYMBOL_INNERS = SYMBOL_STARTS | set(string.digits)
NUMERAL = set(string.digits + '-.')
WHITESPACE = set(' \t\n\r')
DELIMITERS = set('(),:')



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







