#!/usr/bin/env python
# @Author  : pengyun

import operator
from .units import comma_separated


class Expr:
    """
    Basic class
    >>> expr = LambdaExpr(['f'], CallExpr(Name('f'), [Literal(0)]))
    >>> expr
    LambdaExpr(['f'], CallExpr(Name('f'), [Literal(0)]))
    >>> str(expr)
    'lambda f: f(0)'

    >>> expr = CallExpr(LambdaExpr(['x'], Name('x')), [Literal(5)])
    >>> expr
    CallExpr(LambdaExpr(['x'], Name('x')), [Literal(5)])
    >>> str(expr)
    '(lambda x: x)(5)'

    >>> expr = CallExpr(LambdaExpr([], Literal(5)), [])
    >>> expr
    CallExpr(LambdaExpr([], Literal(5)), [])
    >>> str(expr)
    '(lambda: 5)()'
    """
    def __init__(self, *args):
        self.args = args

    def eval(self, env):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        args = '('+ comma_separated([repr(a) for a in self.args]) + ')'
        return type(self).__name__ + args



