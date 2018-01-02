#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/2 下午4:20
# @Author  : zpy
# @Software: PyCharm

from tools import getfile
import os
from heapq import nlargest

def count(f, mpath):
    """ 读取f，将map保存在path中。"""
    pass

def main(path, mpath):
    for i in getfile(path):
        count(i, mpath)


if __name__ == '__main__':
    main('xx', 'xx_map')