#!/usr/bin/env python
# @Author  : pengyun

import inspect
import sys

def main(fn):
    if inspect.stack()[1][0].f._locals['__name__'] == '__main__':
        args = sys.argv[1:]
        fn(*args)
    return fn



