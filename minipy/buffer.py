#!/usr/bin/env python
# @Author  : pengyun


class Buffer:
    """
    >>> buf = Buffer(['(', '+', 15, 12, ')'])
    >>> buf.pop()
    '('
    >>> buf.pop()
    '+'
    >>> buf.current()
    15
    >>> buf.pop()
    15
    >>> buf.current()
    12
    >>> buf.pop()
    12
    >>> buf.pop()
    ')'
    >>> buf.pop()  # returns None
    """
    def __init__(self, source):
        self.index = 0
        self.source = source

    def pop(self):
        current = self.current()
        self.index += 1
        return current

    def current(self):
        if self.index >= len(self.source):
            return None
        else:
            return self.source[self.index]

    def expect(self, expected):
        actual = self.pop()
        if expected != actual:
            raise SyntaxError("expected '{}' but got '{}'".format(expected, actual))
        else:
            return actual

    def __str__(self):
        return str(self.source[self.index:])





