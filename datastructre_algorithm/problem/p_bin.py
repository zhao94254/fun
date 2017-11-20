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