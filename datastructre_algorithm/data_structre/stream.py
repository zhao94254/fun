#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:52
# @Author  : zpy
# @Software: PyCharm


class Stream:
    def __init__(self, first, second=lambda:None):
        assert callable(second), 'must be callable'
        self.first = first
        self.second = second

    @property
    def rest(self):
        """只在第一次调用时计算一次 second"""
        if self.second is not None:
            print('call')
            self._rest = self.second()
            self.second = None
        return self._rest

def integer_stream(first):
    return Stream(first, lambda :Stream(first+1))

def stream_to_list(stream):
    _list = []
    while stream is not None:
        _list.append(stream.first)
        stream = stream.rest
    return _list

def fib_stream(a, b):
    return Stream(a, lambda :fib_stream(b, a+b))


if __name__ == '__main__':

    s = Stream(1, lambda :Stream(2+3, lambda :Stream(1)))
    f = fib_stream(0, 1)

    for i in range(10):
        print(f.first)
        f = f.rest

    print(stream_to_list(s))






