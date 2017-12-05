#!/usr/bin/env python
# @Author  : pengyun

from . import export
from .foo import *

s  = Spam()
print(s)

@export
class A:
    pass

class B:
    pass

class C:
    pass



