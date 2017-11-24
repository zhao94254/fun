#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:51
# @Author  : zpy
# @Software: PyCharm




def is_rotate(s1, s2):
    """
    >>>is_rotate('12345', '34512')
    True
    :param s1:
    :param s2:
    :return:
    """
    if s2 in s1*2:
        return True
    return False

def anagrams(lst):
    def sort_str(s):
        return ''.join(sorted(list(s)))
    _map = {}
    res = []
    for i in lst:
        si = sort_str(i)
        if si not in _map:
            _map[si] = [i]
        else:
            _map[si].append(i)
    for m in _map:
        if len(_map[m]) > 1:
            res += _map[m]
    return res


if __name__ == '__main__':

    print(anagrams(['lint','inlt','intl','fkkk']))









