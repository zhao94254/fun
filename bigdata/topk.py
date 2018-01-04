#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/2 下午4:20
# @Author  : zpy
# @Software: PyCharm

from tools import getfile
import os
from heapq import nlargest

def count(x, f, mpath):
    """ 读取f，将map保存在path中。"""
    res = {}
    mpath = os.path.join(mpath, f)
    with open(mpath, 'wb') as w:
        with open(f, 'rb') as r:
            for i in r.readlines():
                res[i] = res.get(i, 0)+1
        res = nlargest(x, res.items(), lambda x: x[1]) # 直接使用nlargest 获取最大的x个数。
        for i in res:
            w.write(i) # 写入map


def topx(x, path, mpath):
    """ 将所有的都统计一次"""
    res = {}
    for f in getfile(path):
        count(x, f, mpath)

    for m in os.listdir(mpath):
        _map = os.path.join(mpath, m)
        with open(_map, 'r') as f:
            k, v = f.split()
            res[k] = res.get(k, 0)+v

    _topk = nlargest(x, res.items(), lambda x: x[1])
    return _topk

if __name__ == '__main__':
    topx('xx', 'xx_map')