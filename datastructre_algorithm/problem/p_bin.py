#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:52
# @Author  : zpy
# @Software: PyCharm

def count_bin(x):
    """统计x的二进制中1的个数"""
    res = 0
    for i in range(32):
        if x & 1:
            res += 1
        x >>= 1
    return res

def a_to_b(a, b):
    """a 转化为b要改变的二进制位数"""
    return count_bin(a^b)

def is_two_pow(x):
    if x<0:
        return False
    return x&(x-1) == 0


if __name__ == '__main__':
    print(a_to_b(31,14))

    print(is_two_pow(4))