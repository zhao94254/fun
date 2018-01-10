#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/9 下午2:42
# @Author  : zpy
# @Software: PyCharm

import redis
import importlib.util

# importlib.util.find_spec('socket')
#
#  返回一个 ModuleSpec 对象
#  这里可以拿到loader 和 origin 属性
#  通过loader方法可以拿到code 对象，
#  通过origin可以拿到代码文件位置
#


class RedisLoader:
    """redisloader 从redis中加载代码.在import中调用 """
    def __init__(self, origin, conn):
        self.origin = origin
        self.conn = conn

    def exec_module(self, module):
        code = self.conn.get(self.origin)
        exec(code, module.__dict__)

    def create_module(self, spec):
        return None


class RedisImporter:

    def __init__(self, *args, **kwargs):
        self.connection = redis.Redis(*args, **kwargs)
        # 需要先调用一次，否则在下面调用的时候会递归调用。
        self.connection.get('test')

    def find_spec(self, name, path, target=None):
        origin = name + '.py'
        if self.connection.exists(origin):
            loader = RedisLoader(origin, self.connection)
            return importlib.util.spec_from_loader(name, loader)


def enable(*args, **kwargs):
    import sys
    sys.meta_path.insert(0, RedisImporter(*args, **kwargs))


def server_import(name, path):
    """从远程导入。。。"""
    enable()
    name += '.py'
    import requests
    r = redis.Redis()
    r.set(name, requests.get(path).json()['code'])

if __name__ == '__main__':

    server_import('itest', 'https://www.yunxcloud.cn/api/v1/code/33')
    import itest
    itest.getfile('/User/test/py')
