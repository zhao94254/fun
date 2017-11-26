#!/usr/bin/env python
# @Author  : pengyun


def back_pack(m, lst):
    """背包问题。只考虑重量"""
    dp = [0] * (m+1)
    if sum(lst) <= m:
        return sum(lst)
    for i in range(len(lst)):
        for j in range(m, 0, -1):
            if j >= lst[i]:
                dp[j] = max(dp[j], dp[j-lst[i]]+lst[i])
                # 取到最大的可以装的。这里依靠数组来保存了一个之前的状态
    return dp[-1]

def back_pack2(m, lst, value):
    """背包问题。考虑价格"""
    dp = [0] * (m+1)
    if sum(lst) <= m:
        return sum(value)
    for i in range(len(lst)):
        for j in range(m, 0, -1):
            if j >= lst[i]:
                dp[j] = max(dp[j], dp[j-lst[i]]+value[i])
    return dp[-1]
