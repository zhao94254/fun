#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午3:58
# @Author  : zpy
# @Software: PyCharm

import os


def move_stack(n, start, end, tmp):
    """汉诺塔 理解递归&栈"""
    if n == 1:
        print("move {}  from {} --> to {}".format(n, start, end))
    else:
        move_stack(n-1, start,tmp, end)
        print("move {}  from {} --> to {}".format(n, start, end))
        move_stack(n-1, tmp, end, start)


def deep_len(lst):
    """
    返回一个有多级嵌套列表的长度
    >>> x = [1,2,[3,4,[3,4,6]]]
    >>>deep_len(x)
    7
    :param lst
    :return:
    """
    len_lst = 0
    def helper(lst):
        nonlocal len_lst
        for i in lst:
            if isinstance(i, list):
                helper(i)
            else:
                len_lst += 1
    helper(lst)
    return len_lst

def getfile(filetmp):
    """获取指定文件夹下所有的文件"""
    res = []
    import os
    def helper(filetmp):
        for i in os.listdir(filetmp):
            i = os.path.join(filetmp, i)
            if os.path.isfile(i):
                res.append(i)
            else:
                helper(i)
        return res
    return helper(filetmp)