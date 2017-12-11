#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:52
# @Author  : zpy
# @Software: PyCharm


class Stream:
    """流 。。"""
    def __init__(self, first, second=lambda:None):
        assert callable(second), 'must be callable'
        self.first = first
        self.second = second

    @property
    def rest(self):
        """只在第一次调用时计算一次 second"""
        if self.second is not None:
            self._rest = self.second()
            self.second = None
        return self._rest



if __name__ == '__main__':

    s = Stream(1, lambda :Stream(2+3, lambda :Stream(1)))







