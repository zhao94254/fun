#!/usr/bin/env python
# @Author  : pengyun
# 用来将分析后的单词构造为具体的表达式

import operator
from units import comma_separated

# Expr
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
    """返回一个数字"""
    def __init__(self, value):
        Expr.__init__(self, value)
        self.value = value

    def eval(self, env):
        return Number(self.value)

    def __str__(self):
        return str(self.value)


class Name(Expr):
    """ Name 是一个变量"""
    def __init__(self, string):
        Expr.__init__(self, string)
        self.string = string

    def eval(self, env):
        """
        >>> env = {'a':Number(1), 'b': Number(3)}
        >>> Name('a').eval(env)
        1
        :param env:
        :return:
        """
        if self.string not in env:
            raise NameError("{} not in env".format(self.string))
        return env[self.string]


class LambdaExpr(Expr):
    def __init__(self, parameters, body):
        Expr.__init__(self, parameters, body)
        self.parameters = parameters
        self.body = body

    def eval(self, env):
        return LambdaFunction(self.parameters, self.body, env)

    def __str__(self):
        body = str(self.body)
        if not self.parameters:
            return 'lambda: ' + body
        else:
            return 'lambda ' + comma_separated(body)


class CallExpr(Expr):
    def __init__(self, operator, operands):
        Expr.__init__(self, operator, operands)
        self.operator = operator
        self.operands = operands

    def eval(self, env):
        """
        首先时获取到 操作符 操作数。然后global_env获取到真正
        可以操作的来执行。
        >>>_env = global_env.copy()
        >>> _env.update({'a': Number(1), 'b': Number(2)})
        >>> add = CallExpr(Name('add'), [Literal(3), Name('a')])
        >>> add.eval(_env)
        Number(4)
        :param env:
        :return:
        """
        # 支持def
        function = self.operator.eval(env)

        if isinstance(self.operator, Name) and self.operator.string == 'def':
            operators = [o.string for o in self.operands if isinstance(o, Name)]
            operands = [o.eval(env) for o in self.operands if isinstance(o, Literal)]
            return function.operator(env, operators, operands)
        arguments = [o.eval(env) for o in self.operands]
        return function.apply(arguments)

    def __str__(self):
        function = str(self.operator)
        args = '(' + comma_separated(self.operands) + ')'
        if isinstance(self.operands, LambdaExpr):
            return '(' + function + ')' + args
        else:
            return function + args


# Value

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
    """ 返回一个数字 """
    def __init__(self, value):
        Value.__init__(self, value)
        self.value = value

    def apply(self, arguments):
        raise TypeError("Cannot apply number{} to arguments {}".format(
            self.value, comma_separated(arguments)
        ))

    def __str__(self):
        return str(self.value)


class LambdaFunction(Value):
    """ 创建一个lambda function 通过lambdaexpr.expr 来执行，"""
    def __init__(self, parameters, body, parent):
        Value.__init__(self, parameters, body, parent)
        self.parameters = parameters
        self.body = body
        self.parent = parent

    def apply(self, arguments):
        """
        将参数绑定到lambda 的 变量中。
        :param arguments:
        :return:
        """
        if len(self.parameters) != len(arguments):
            raise TypeError("Cannot match parameters {} to arguments {}".format(
                comma_separated(self.parameters), arguments
            ))
        env = self.parent.copy()
        for p, a in zip(self.parameters, arguments):
            env[p] = a
        return self.body.eval(env)

    def __str__(self):
        definition = LambdaExpr(self.parameters, self.body)
        return "<function {}>".format(definition)


class PrimitiveFunction(Value):
    """提供一些内置函数。"""
    def __init__(self, operator):
        Value.__init__(self, operator)
        self.operator = operator

    def apply(self, arguments):
        for a in arguments:
            if not isinstance(a, Number):
                raise TypeError("Invalid argument {} to {}".format(
                    comma_separated(arguments), self
                ))
        return Number(self.operator(*[a.value for a in arguments]))

    def __str__(self):
        return '<primitive function {}>'.format(self.operator.__name__)


# 内置函数，可以根据需要自己添加

fact = lambda x: 1 if x == 1 else fact(x-1) * x

def do_define(env, operators, operands):
    import pdb
    pdb.set_trace()
    if len(operators) != len(operands):
        raise SyntaxError("Not match")
    for i, j in zip(operators, operands):
        env[i] = j
    return


global_env = {
    'abs': PrimitiveFunction(operator.abs),
    'add': PrimitiveFunction(operator.add),
    'float': PrimitiveFunction(float),
    'floordiv': PrimitiveFunction(operator.floordiv),
    'int': PrimitiveFunction(int),
    'max': PrimitiveFunction(max),
    'min': PrimitiveFunction(min),
    'mod': PrimitiveFunction(operator.mod),
    'mul': PrimitiveFunction(operator.mul),
    'pow': PrimitiveFunction(pow),
    'sub': PrimitiveFunction(operator.sub),
    'truediv': PrimitiveFunction(operator.truediv),
    # self define
    'fact': PrimitiveFunction(fact),
    'def': PrimitiveFunction(do_define),
}

