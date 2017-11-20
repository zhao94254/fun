#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午2:02
# @Author  : zpy
# @Software: PyCharm


def max_subarray(nums):
    """ 最大子数组 """
    if all(map(lambda x:x<0), nums):
        return max(nums)
    res, tmp = 0, 0
    for i in nums:
        tmp += i
        res = max(res, tmp)
        if tmp < 0:
            tmp = 0
    return res


def sub_sum_zero(nums):
    """和为0的子数组 思路 用一个map来保存之前"""
    _map = {0:-1}
    t = 0
    for i, j in enumerate(nums):
        t += j
        if t in _map:
            return [_map[t]+1, i]
        _map[t] = i
    return


def max_x_array(x, array):
    """求长为x的最大子数组"""
    tmp, res = 0, 0
    for i in range(len(array)-x):
        tmp = sum(array[i:i+x])/x
        res = max(res, tmp)
    return res



if __name__ == '__main__':
    data = [-5,10,5,-3,1,1,1,-2,3,-4]
    max_subarray(data)
    max_x_array(3, data)
    sub_sum_zero(data)
