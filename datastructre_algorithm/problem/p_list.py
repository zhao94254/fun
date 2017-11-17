#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午2:02
# @Author  : zpy
# @Software: PyCharm




def subarraySum(nums):
    """和为0的子数组"""
    _map = {0:-1}
    t = 0
    for i, j in enumerate(nums):
        t += j
        if t in _map:
            return [_map[t]+1, i]
        _map[t] = i
    return

# print(subarraySum([-5,10,5,-3,1,1,1,-2,3,-4]))
