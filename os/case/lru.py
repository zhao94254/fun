#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/18 下午6:47
# @Author  : zpy
# @Software: PyCharm


from collections import OrderedDict


class LRUCache:
    """lru 算法实现，通过orderdict 来实现。"""
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        # 将用过的key再次插到最前面
        value = -1
        if key in self.cache:
            value = self.cache.pop(key)
            self.cache[key] = value
            return value
        else:
            return value

    def set(self, key, value):
        # 如果已经在cache中，更新为新的，如果不在将最久未使用的放入
        if key in self.cache:
            self.cache.pop(key)
            self.cache[key] = value
        else:
            if len(self.cache) == self.capacity:
                self.cache.popitem(last=False)
                self.cache[key] = value
            else:
                self.cache[key] = value













