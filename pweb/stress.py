#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/10 下午4:47
# @Author  : zpy
# @Software: PyCharm

import requests
import inspect

class Query:
    """
    Single test. 负责单个任务
    所有的测试函数以check_ 开头, 返回 true or false
    check 最后返回结果
    """
    def __init__(self, url):
        self.session = requests.session()
        self.url = url

    def check_test(self):
        return True

    def getmethods(self):
        return inspect.getmembers(self, predicate=inspect.ismethod)

    def check(self):
        """ 返回是否全部成功， 和成功率"""
        methods = self.getmethods()
        _check = [m for m in methods if m[0].startswith('check_')]
        all_check = len(_check)
        success_check = len([m[1] for m in _check if m[1]])
        rate = success_check / all_check
        return rate == 1, rate

if __name__ == '__main__':
    q = Query('x')
    print(q.check())