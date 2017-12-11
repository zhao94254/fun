#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/11 下午2:45
# @Author  : zpy
# @Software: PyCharm

from inspect import getsource, getmembers, isfunction, isclass
import importlib
import importlib.util
import sys
import os
import pprint


def find_function(module, fname=None):
    """根据名字，获取指定的函数。约定doc开头是函数解释，或者中文名"""
    res = []
    if fname is None: # 返回全部的函数名
        return [i[0] for i in getmembers(module) if isfunction(i[1])]
    for _, i in getmembers(module):
        if isfunction(i) or isclass(i):
            if (i.__name__ == fname or (i.__doc__ and fname in i.__doc__)):
                res.append(getsource(i))
    return res


def getfile(path, end=None):
    """获取指定路径下的 以end结尾的file"""
    res = []
    def helper(path):
        for i in os.listdir(path):
            i = os.path.join(path, i)
            if os.path.isfile(i):
                if end and i.endswith(end):
                    res.append(i)
                elif end is None:
                    res.append(i)
            else:
                helper(i)
    helper(path)
    return res

def self_import(path):
    """直接导入py文件"""
    name = path.split('.')[0].split('/')[-1]
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[name] = module
    return module

def getfunc(path, name):
    """根据path, name 寻找对应的函数"""
    for i in getfile(path, 'py'):
        module= self_import(i)
        res = find_function(module, name)
        if len(res) > 0:
            pprint.pprint(res)
            return
    print("can't find")

if __name__ == '__main__':
    getfunc('/Users/mioji/Desktop/py/github/fun/ds_algorithm', "背包")






