#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午3:58
# @Author  : zpy
# @Software: PyCharm


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

def permute(s):
    """全排列"""
    res = []
    def helper(s, start):
        if start >= len(s):
            res.append(s[:])
        for i in range(start, len(s)):
            s[i], s[start] = s[start], s[i]
            helper(s, start+1)
            s[i], s[start] = s[start], s[i]
    helper(s, 0)
    return res

def depthsum(lst):
    """
    嵌套列表的加权和
    :param lst:  [1,[2,2,3],3]
    :return: 18
    """
    res = 0
    def helper(x, d):
        nonlocal res
        if len(x) == 0:
            return
        sb = x[0]
        if not isinstance(sb, list):
            res += sb*d
        else:
            helper(x[0], d+1)
        helper(x[1:], d)
    helper(lst, 1)
    return res

if __name__ == '__main__':
    # print(permute([1,2,3]))
    print(depthsum([1,[2,2,3],3]))