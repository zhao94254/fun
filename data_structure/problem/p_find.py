#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/21 下午1:48
# @Author  : zpy
# @Software: PyCharm


def find_position(data, target):
    """二分搜索"""
    l, r = 0, len(data)
    while l<r:
        m = (l+r) // 2
        if target == data[m]:
            return m
        elif target > data[m]:
            l = m+1
        else:
            r = m-1
    return -1
