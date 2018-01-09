#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/9 下午5:24
# @Author  : zpy
# @Software: PyCharm

from redisloader import enable
import redis

enable()
r = redis.Redis()
r.set('foo.py', 'print("imported foo")')
import foo

print(foo)