#!/usr/bin/env python
# @Author  : pengyun

from reader import read
from expr import global_env
from units import main

read_only = False

code = [
    '(lambda x: add(x, 10))(10)',
    'add(2,3)',
    'def(x,100)',
    'max(1,2,3,x)',
    'fact(100)',
]

@main
def start():
    for c in code:
        expr = read(c)
        if read_only:
            print(repr(expr))
        else:
            print(expr.eval(global_env))

