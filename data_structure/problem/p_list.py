#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午2:02
# @Author  : zpy
# @Software: PyCharm

def triangle_count(lst):
    """ 给一个列表，返回可以组成三角形的个数.
    思路：将列表排序，每次先找到最大的一条边。然后从之前开始找
    符合条件的一个区间的
    """
    res = 0
    if len(lst) < 3:
        return 0
    lst.sort()
    for i in range(2, len(lst)):
        longest = lst[i]
        l, r = 0, i-1
        while l < r:
            if lst[l]+lst[r] <= longest: # 如果小于，向右走
                l += 1
            else:
                res += r-l
                r -= 1
    return res

def max_subarray(nums):
    """ 最大子数组 """
    if all(map(lambda x:x<0, nums)):
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

def lcs(a, b):
    """ 最长公共子串"""
    tmp = [[0]* (len(b)+1) for _ in range(len(a)+1)]
    for i in range(len(a)):
        for j in range(len(b)):
            if a[i] == b[j]:
                tmp[i][j] = tmp[i-1][j-1]+1
            else:
                tmp[i][j] = max(tmp[i][j-1], tmp[i-1][j])
    return tmp[-2][-2]

def lics(lst):
    """最长连续上升子序列"""
    if len(lst) == 0:
        return 0
    def helper(lst):
        res, tmp = 0, 0
        for i in range(1, len(lst)):
            if lst[i] > lst[i-1]:
                tmp += 1
            else:
                tmp = 0
            res = max(res, tmp)
        return res+1
    return max(helper(lst), helper(lst[::-1]))

def median(lst):
    """ 中位数"""
    lst.sort()
    lent = len(lst)
    if lent % 2:
        return lst[lent/2]
    return lst[lent/2-1]

def add_digits(num):
    """ 38-->3 8-->11-->2.将各位数相加，转为一个比10小的数
    >>>add_digits(38)
    2
    """
    def helper(num):
        res = []
        while num > 0:
            res.append(num%10)
            num //= 10
        return sum(res)

    while True:
        res = helper(num)
        num = res
        if res < 10:
            return res

def wiggle_sort(lst):
    """ nums[0] <= nums[1] >= nums[2] <= nums[3]...
    奇数位的大于之前的，偶数位的小于之前的。
    """
    for i in range(1, len(lst)):
        if (i%2 == 0 and lst[i] > lst[i-1]) or (i%2 and lst[i] < lst[i-1]):
            lst[i], lst[i-1] = lst[i-1], lst[i]
    return lst

def max_square(lst):
    """求一个二维01矩阵中全为1的最大正方形"""
    res = 0
    tmp = lst[:]
    m, n = len(lst), len(lst[0])
    for i in range(1, m): # 判断当前位置之前的三个位置
        for j in range(1, n):
            if lst[i][j] == 0:
                tmp[i][j] = 0
            else: # 当前位置为1，将前面的位置的数加上
                tmp[i][j] = min(lst[i-1][j], lst[i-1][j-1], lst[i][j-1])+1
    for i in range(m):
        for j in range(n):
            res = max(tmp[i][j], res)
    return res*res

def largest_area(lst):
    """ 直方图最大矩阵覆盖 通过单调栈来解决"""
    stack = []
    res, i = 0, 0
    while i < len(lst):
        # 存入递增序列的末位
        if len(stack) == 0 or lst[stack[-1]] < lst[i]:
            stack.append(i)
        else:
            start = stack.pop()
            width = i if not stack else i-stack[-1]-1 # 获得宽度，通过单调栈中的下标位置计算出来。
            res = max(res, lst[start]*width) # 计算矩阵大小
            i -= 1
        i += 1
    while stack:
        start = stack.pop()
        width = i if not stack else i-stack[-1]-1
        res = max(res, lst[start]*width)
    return res

def trip_rainwater(lst):
    """  接雨水。思路用四个指针来记录。"""
    res = 0
    l, r, lmax, rmax = 0, len(lst)-1, 0, 0
    while l < r:
        lmax = max(lmax, lst[l]) # 记录左面的高点
        rmax = max(rmax, lst[r]) # 右面的高点
        if lmax < rmax:
            res += lmax-lst[l] # 坑的大小
            l += 1
        else:
            res += rmax-lst[r]
            r -= 1
    return res

class NestIter:
    def __init__(self, nlst):
        self.nlst = nlst

    def next(self):
        for i in self.nlst:
            if isinstance(i, list):
                pass

    def hasnext(self):
        pass

def flatten(lst):
    """多维降为一维"""
    for i in lst:
        if isinstance(i, list):
            yield from flatten(i)
        else:
            yield i

def max_sub(lst):
    """最大子数组差"""
    res = 0
    for i in range(1, len(lst)):
        res = max(res, find_max(lst[:i]) - find_min(lst[i:]))
    return res

def find_max(lst):
    res = 0
    tmp = 0
    for i in lst:
        tmp += i
        if tmp < 0:
            tmp = 0
        else:
            res = max(res, tmp)
    return res

def find_min(lst):
    res = 0
    tmp = 0
    for i in lst:
        tmp += i
        if tmp > 0:
            tmp = 0
        res = min(tmp, res)
    return res

def max_profit(prices):
    """
    股票交易 - 可以交易多次
    解决思路 优先队列
    :param prices:
    :return:
    """
    _q = []
    res = 0
    for d in prices:

        if len(_q) > 0:
            top = min(_q)
            if d > top:
                _q.remove(top)
                res += (d-top)
                _q.append(d) # append 两次是为了获取全局最优解
        _q.append(d)
    return res

if __name__ == '__main__':
    data = [-5, 10, 5, -3, 1, 1, 1, -2, 3, -4]
    max_subarray(data)
    max_x_array(3, data)
    sub_sum_zero(data)
    # print(lcs('asdfjshadkjfhkahsdkf', 'asdfjklsadjlfjlskd'))
    print(largest_area([21,2,23,12,25,26,27,15,20]))
    print(trip_rainwater([0,1,0,2,1,0,1,3,2,1,2,1]))










