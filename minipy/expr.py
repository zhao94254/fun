#!/usr/bin/env python
# @Author  : pengyun
# 用来将分析后的单词构造为具体的表达式

import operator
from .units import comma_separated


class Expr:
    """
    Basic class, 将输入经过tokenize后，转化为具体的表达式。
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


class Literal(Expr):
    pass


class Name(Expr):
    pass


class Value:
    """
    value 是 表达式执行后的结果。
    在这个程序中 主要有：
    numbers ： 12
    lambda function： lambda x：x+1
    primitive function： add mul
    """
    def __init__(self, *args):
        self.args = args

    def apply(self, arguments):
        raise NotImplementedError

    def __str__(self):
        raise NotImplementedError

    def __repr__(self):
        args  = '(' + comma_separated([repr(arg) for arg in self.args ]) + ')'
        return type(self).__name__ + args

class Number(Value):
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, arguments):
        raise TypeError("Cannot apply number{} to arguments {}".format(
            self.value, comma_separated(arguments)
        ))




