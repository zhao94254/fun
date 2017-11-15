#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/15 下午7:21
# @Author  : zpy
# @Software: PyCharm


def two_sum(numbers, target):
    """ two sum """
    for i, num in enumerate(numbers):
        tmp = target - num
        if tmp in numbers:
            return [i+1, numbers.index(tmp)+1]
    return []

def three_sum(numbers, target):
    """ three sum"""
    for i, num in enumerate(numbers):
        f = target - num
        res = two_sum(numbers[i+1:], f)
        if len(res) > 0:
            return [i, res[0]+i, res[1]+i]
    return []


print(three_sum(list(range(10)), 6))


