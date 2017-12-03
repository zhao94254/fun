#!/usr/bin/env python
# @Author  : pengyun

import weakref
from .. import

class Spam:
    if 'Spam' in globals():
        _instance = Spam._instance
    else:
        _instance = weakref.WeakSet()

    def __init__(self):
        Spam._instance.add(self)

    def yow(self):
        print("new yow")

