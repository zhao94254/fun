#!/usr/bin/env python
# @Author  : pengyun

def convert(n, x):
    """
    N 进制转化， 直接使用ascii码中的字符来代替了"
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





