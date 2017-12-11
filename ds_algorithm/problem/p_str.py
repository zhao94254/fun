#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:51
# @Author  : zpy
# @Software: PyCharm

def find_str(s, target):
    """在s中查找target 并返回target在s中的起始位置"""
    lent = len(target)
    for i in range(len(s)-lent):
        if s[i: i+lent] == target:
            return i
    return -1

def unique_s(s):
    """判断字符串是否有重复字符。"""
    return len(set(s)) == len(s)

def is_rotate(s1, s2):
    """
    变位词判断
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
    """乱序字符串"""
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

def lcp(strs):
    """返回最长公共前缀"""
    res = ''
    tmp = ''
    for i in zip(*strs):
        if len(set(i)) == 1:
            tmp += i[0]
        else:
            tmp = ''
        res = res if len(res) > len(tmp) else tmp
    return res



if __name__ == '__main__':

    print(anagrams(['lint','inlt','intl','fkkk']))
    print(lcp(['abcd','abcdd','abe']))








