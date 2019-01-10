#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午6:55
# @Author  : zpy
# @Software: PyCharm


def d_inject(arr, i, j, n, m):
    """dfs 标记"""
    if i<0 or i>=n or j<0 or j>=m or arr[i][j]!=1:
        return
    arr[i][j] = 2
    d_inject(arr, i - 1, j, n, m)
    d_inject(arr, i + 1, j, n, m)
    d_inject(arr, i, j - 1, n, m)
    d_inject(arr, i, j + 1, n, m)


def b_inject(arr, i, j, n, m):
    """bfs 标记"""
    tmp = [[i,j]]
    while len(tmp)>0:
        i, j = tmp.pop()
        arr[i][j] = 2
        if i >= n or j >= m:
            break
        if i<n-1 and arr[i+1][j] == 1:
            tmp.append([i+1, j])
        if i>0 and arr[i-1][j] == 1:
            tmp.append([i-1, j])
        if j<m-1 and arr[i][j+1] == 1:
            tmp.append([i, j+1])
        if j>0 and arr[i][j-1] == 1:
            tmp.append([i, j-1])


def count_lands(data):
    """岛屿统计，统计一个01数组中1构成的岛屿数量"""
    res = 0
    n, m = len(data), len(data[0])
    for i in range(n):
        for j in range(m):
            if data[i][j] == 1:
                res += 1
                b_inject(data, i, j, n, m)
                # d_inject(data, i, j, n, m)
    return res

def d_json(data, key):
    """通过key 来寻找json中对应的数据。 dfs版本"""
    res = []
    def help(data, key):
        if isinstance(data, dict):
            for k in data.keys():
                if k == key:
                    res.append(data[k])
                else:
                    if isinstance(data[k], dict):
                        help(data[k], key)
                    if isinstance(data[k], list):
                        for i in data[k]:
                            help(i, key)
        elif isinstance(data, list):
            for i in data:
                help(i, key)
    help(data, key)

    return len(res), res

def b_json(data, key):
    """通过key 来寻找json中对应的数据。 bfs版本"""
    queue = [data]
    res = []
    while len(queue) > 0:
        f = queue.pop(0)
        if isinstance(f, dict):
            for k in f.keys():
                if k == key:
                    res.append(f[k])
                elif isinstance(f[k], dict):
                    queue.append(f[k])
                elif isinstance(f[k], list):
                    queue.extend(f[k])
                else:
                    pass
        elif isinstance(f, list):
            queue.extend(f)
    return res, len(res)

def reach_end(_map):
    """
    给一个地图，问是否可以走到终点
    :param _map:
    :return:
    """
    m, n = len(_map), len(_map[0])
    st = [(0,0)]
    while st:
        p, e = st.pop(0)
        if p + 1 == m:
            if _map[p][e+1] == 1:
                st.append((p, e+1))
            elif _map[p][e+1] == 9:
                return True
            continue
        if e + 1 == m:
            if _map[p+1][e] == 1:
                st.append((p+1, e))
            elif _map[p+1][e] == 9:
                return True
            continue
        if _map[p+1][e]==9 or _map[p][e+1]==9:
            return True
        if _map[p+1][e] == 1:
            st.append((p+1,e))
        if _map[p][e+1] == 1:
            st.append((p, e+1))
    return False

if __name__ == '__main__':
    data = [
      [1, 1, 0, 0, 0],
      [0, 1, 0, 0, 1],
      [0, 0, 0, 1, 1],
      [0, 0, 0, 0, 0],
      [0, 0, 0, 0, 1]
    ]
    # d_inject(data, 0, 0, 5, 5)
    print(count_lands(data))
    print(data)














