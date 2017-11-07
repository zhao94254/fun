#!/usr/bin/env python
# @Author  : pengyun

from units import main
import sys

from reader import read
from expr import global_env


if __name__ == '__main__':
    read_only = len(sys.argv) == 2 and sys.argv[1] in ('--read', '-r')
    while True:
        try:
            user_input = input('>')
            expr = read(user_input)
            if expr is not None:
                if read_only:
                    print(repr(expr))
                else:
                    print(expr.eval(global_env))
        except (SyntaxError, NameError, TypeError) as e:
            print(type(e).__name__ + ':', e)
        # ctrl -c ctrl -d
        except (KeyboardInterrupt, EOFError):
            print()
            break