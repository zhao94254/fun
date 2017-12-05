#!/usr/bin/env python
# @Author  : pengyun

__all__ = []

def export(defn):
    globals()[defn.__name__] = defn
    __all__.append(defn.__name__)
    return defn

from . import testf
