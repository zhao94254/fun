#!/usr/bin/env python
# @Author  : pengyun

import inspect
import sys

def main(fn):
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:]
        fn(*args)
    return fn


def comma_separated(xs):
    """
    将列表转化为字符串
    >>> comma_separated(['spam', 5, False])
    'spam, 5, False'
    >>> comma_separated([5])
    '5'
    >>> comma_separated([])
    ''
    """
    return ', '.join([str(x) for x in xs])


