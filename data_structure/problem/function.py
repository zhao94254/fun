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


def trail_zero(n):
    """统计N的阶乘后0的个数"""
    res = 0
    while n > 0:
        res += n // 5
        n = n // 5
    return res


def mulitipy(a, b):
    """ 大数相乘 i位*j位 等于i+j位"""
    a = [int(i) for i in a][::-1]
    b = [int(j) for j in b][::-1]
    res = [0] * len(a+b)
    for i in range(len(a)):
        for j in range(len(b)):
            res[i+j] = a[i]*a[j]
    for i in range(len(res)):
        if res[i] > 9:
            res[i+1] += res[i] // 10 # 进位
            res[i] = res[i] % 10
    return res

def swap_(x, n):
    """不使用辅组空间将x中的元素按照n划分"""
    if n not in x:
        print("....")
        return
    l = 0
    for i in range(len(x)):
        if x[i] < n:
            x[i], x[l] = x[l], x[i]
            l += 1
    k = x.index(n)
    x[k], x[l] = x[l], x[k]
    print(x, l, n)

def mul_set(lst):
    """
    对列表的多个集合取交集
    :param lst:
    :return:
    """
    tmp = lst[0]
    for i in range(1, len(lst)):
        tmp = lst[i] & tmp
    return tmp

def combine(lst, n):
    """
    组合
    通过递归实现
    :param lst:
    :return:
    """
    res = []
    tmp = [0] * n
    def helper(cur, ni):
        if ni == n:
            res.append(tmp[:])
            return
        for i in range(cur, len(lst)):
             tmp[ni] = lst[i]
             helper(cur+1, ni+1)
    helper(0, 0)
    return res

if __name__ == '__main__':
    print(combine([1,2,3,4,5], 2))