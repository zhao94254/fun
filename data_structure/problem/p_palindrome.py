#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午3:57
# @Author  : zpy
# @Software: PyCharm


def is_palindrome(s):
    """检查是否是一个回文串"""
    return s == s[::-1]

def longest_palindrome(s):
    """最长回文 O(n2)"""
    res = 0
    if len(s) < 2:
        return s
    for i in range(len(s)): # 长度为奇数时的处理方法
        j, k = i-1, i+1
        while j >=0 and k<len(s) and s[j]==s[k]:
            if res < k-j+1:
                res = k-j+1
                start = j
            j -= 1
            k += 1
    for i in range(len(s)): # 偶数时的方法
        j, k = i, i+1
        while j >=0 and k<len(s) and s[j]==s[k]:
            if res < k-j+1:
                res = k-j+1
                start = j
            j -= 1
            k += 1
    return s[start: start+res]

if __name__ == '__main__':
    print(longest_palindrome('asjdlfkjskladjlabcdedcbaa'))










