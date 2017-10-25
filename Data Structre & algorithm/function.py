#!/usr/bin/env python
# @Author  : pengyun

def convert(n, x):
    """
    在短网址系统会使用到这样的一个转化，将一个大的十进制数转化为一个
    短的高进制的数。常用的转化是62进制。[Aa-Zz, 0-9]
    N 进制转化， 直接使用ascii码中的字符来代替了。
    :param n:  N进制
    :param x:  一个十进制的数
    :return:
    >>>convert(62, 563453245)
    V8;iS
    """
    tmp = [chr(48+i) for i in range(n)]
    res = ''
    while x > 0:
        res += tmp[x % n]
        x = x//n
    print(res[::-1])


def max_num(array):
    """
    最大连续子数组，考虑到全为负数的情况
    :param array:
    :return:
    """
    if len(array) == len([i for i in array if i<0]):
        return max(array)
    res, tmp = 0, 0
    for i in array:
        tmp += i
        res = max(res, tmp)
        if tmp < 0:
            tmp = 0
    return res

def max_subarray(x, array):
    """求长为x的最大子数组"""
    tmp, res = 0, 0
    for i in range(len(array)-x):
        tmp = sum(array[i:i+x])/x
        res = max(res, tmp)
    return res





