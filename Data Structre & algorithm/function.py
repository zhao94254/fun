#!/usr/bin/env python
# @Author  : pengyun

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
    tmp = [chr(48+i) for i in range(n)]
    res = ''
    while x > 0:
        res += tmp[x % n]
        x = x//n
    print(res[::-1])


def max_num(array):
    """
    最大连续子数组，考虑到全为负数的情况
    :param array:
    :return:
    """
    if len(array) == len([i for i in array if i<0]):
        return max(array)
    res, tmp = 0, 0
    for i in array:
        tmp += i
        res = max(res, tmp)
        if tmp < 0:
            tmp = 0
    return res

def max_subarray(x, array):
    """求长为x的最大子数组"""
    tmp, res = 0, 0
    for i in range(len(array)-x):
        tmp = sum(array[i:i+x])/x
        res = max(res, tmp)
    return res

def move_stack(n, start, end, tmp):
    """汉诺塔 理解递归&栈"""
    if n == 1:
        print("move {}  from {} --> to {}".format(n, start, end))
    else:
        move_stack(n-1, start,tmp, end)
        print("move {}  from {} --> to {}".format(n, start, end))
        move_stack(n-1, tmp, end, start)


def deep_len(lst):
    """
    返回一个有多级嵌套列表的长度
    >>> x = [1,2,[3,4,[3,4,6]]]
    >>>deep_len(x)
    7
    :param lst
    :return:
    """
    len_lst = 0
    def helper(lst):
        nonlocal len_lst
        for i in lst:
            if isinstance(i, list):
                helper(i)
            else:
                len_lst += 1
    helper(lst)
    return len_lst

def getfile(filetmp):
    """获取指定文件夹下所有的文件"""
    res = []
    import os
    def helper(filetmp):
        for i in os.listdir(filetmp):
            i = os.path.join(filetmp, i)
            if os.path.isfile(i):
                res.append(i)
            else:
                helper(i)
        return res
    return helper(filetmp)

def reorder_lst(lst):
    """将奇数放在前面，并保持相对位置不变"""
    return [i for i in lst if i%2 ] + [i for i in lst if i%2==0 ]

def josephus(n, m):
    """约瑟夫环问题"""
    if n == 0 or m == 0:
        return -1
    m -= 1
    p = 0
    while n:
        p = (p+m)%len(n)
        if len(n) == 1:
            return n[0]
        del n[p]


def is_symmetrical(tree1, tree2):
    """检查两个树是否互为镜像树"""
    def helper(l, r):
        if l is None and r is None:
            return True
        if l is None or r is None:
            return False
        if l.val != r.val:
            return False
        return helper(l.left, r.right) and helper(l.right, r.left)
    if tree1 is None and tree2 is None:
        return True
    return helper(tree1.left, tree2.right)









