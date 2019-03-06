#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/15 下午7:21
# @Author  : zpy
# @Software: PyCharm




def two_sum(numbers, target):
    """ 两数相加
        @param numbers : An array of Integer
        @param target : target = numbers[index1] + numbers[index2]
        @return : [index1 + 1, index2 + 1] (index1 < index2)
    """
    for i, num in enumerate(numbers):
        tmp = target - num
        t = i+1
        if tmp in numbers[t:]:
            return [i+1, t+numbers[i+1:].index(tmp)+1]
    return []

def three_sum(numbers, target):
    """ 三数相加"""
    for i, num in enumerate(numbers):
        f = target - num
        res = two_sum(numbers[i+1:], f)
        if len(res) > 0:
            return [i, res[0]+i, res[1]+i]
    return []


if __name__ == '__main__':
    print(two_sum([0,4,3,0], 0))
    print(three_sum(list(range(10)), 6))


