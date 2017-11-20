#!/usr/bin/env python
# @Author  : pengyun

# 一些代码练习

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
    tmp = [chr(48 + i) for i in range(n)]
    res = ''
    while x > 0:
        res += tmp[x % n]
        x = x // n
    print(res[::-1])


def reorder_lst(lst):
    """将奇数放在前面，并保持相对位置不变"""
    return [i for i in lst if i % 2] + [i for i in lst if i % 2 == 0]


def josephus(n, m):
    """约瑟夫环问题"""
    if n == 0 or m == 0:
        return -1
    m -= 1
    p = 0
    while n:
        p = (p + m) % len(n)
        if len(n) == 1:
            return n[0]
        del n[p]
