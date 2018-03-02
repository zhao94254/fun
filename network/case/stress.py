#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/1/10 下午4:47
# @Author  : zpy
# @Software: PyCharm

import requests
import inspect
import time
import redis
from multiprocessing.pool import Pool, ThreadPool
from multiprocessing import Process
import signal
import collections


redis_db = redis.Redis()

PRE = 'stress:test:'
NAME = 'flask'

SUCCESS_KEY = PRE + '{}:success'.format(NAME)
FAILURE_KEY = PRE + '{}:failure'.format(NAME)
TIME_KEY = PRE + '{}:time'.format(NAME)
RATES = PRE + '{}:rates'.format(NAME)

class BaseQuery:
    """
    Single test. 负责单个任务
    所有的测试函数以check_ 开头, 返回 true or false
    check 最后返回结果
    """
    def __init__(self, url=None):
        self.session = requests.session()
        self.url = url

    # def check_testa(self):
    #     return False
    #
    # def check_test(self):
    #     return True

    def getmethods(self):
        return inspect.getmembers(self, predicate=inspect.ismethod)

    def check(self):
        """ 返回是否全部成功， 和成功率"""
        methods = self.getmethods()
        _check = [m for m in methods if m[0].startswith('check_')]
        all_check = len(_check)
        success_check = len([1 for m in _check if m[1]()])
        rate = success_check / all_check
        return rate == 1, rate

def job(queue):
    """
    保存单个任务花费时间， 成功数量， 单个任务成功率
    :param query: 一个query的实例
    :return:
    """
    q = queue()
    start = time.time()
    try:
        ok, rate = q.check()
    except:
        ok, rate = False, 0

    end = time.time()
    cost = end - start
    with redis_db.pipeline() as p:
        if ok:
            p.incr(SUCCESS_KEY)
        else:
            p.incr(FAILURE_KEY)
        p.lpush(RATES, rate)
        p.lpush(TIME_KEY, cost)
        p.execute()

def get_value_num(key):
    v = redis_db.get(key)
    return 0 if v is None else int(v)

def get_range_num(key):
    v = redis_db.lrange(key, 0, -1)
    return [float(i) for i in v]

def divide(n, m):
    """ 将n 分成m份。"""
    avg = n // m
    res = [avg] * m
    for i in range(n%m):
        res[i] += 1
    return res

def thread(threads, queue, num):
    """ 开启多少个任务"""
    pool = ThreadPool(threads)
    for _ in range(num):
        pool.apply_async(job, (queue,))
        time.sleep(0.001)
    pool.close()
    pool.join()

def progress():
    try:
        prev = 0
        while True:
            time.sleep(1)
            cur = get_value_num(SUCCESS_KEY)

            msg = "Per Second: {:4d}/s".format(cur - prev)
            print(msg, end='')
            print('\r' * len(msg), end='')
            prev = cur

    except KeyboardInterrupt:
        pass
    finally:
        print('\n')


def work(task, processes, threads, times):
    pool = Pool(processes,
                lambda: signal.signal(signal.SIGINT, signal.SIG_IGN))
    p = Process(target=progress)
    p.daemon = True

    start = time.time()
    try:
        for chunk in divide(times, processes):
            pool.apply_async(thread, (threads, task, chunk))

        p.start()

        pool.close()
        pool.join()
        p.terminate()
        p.join()

    except KeyboardInterrupt:
        # pool.terminate()
        p.terminate()
        p.join()
        # pool.join()

    return time.time() - start


def report(processes, threads, name, pre):
    success = get_value_num(SUCCESS_KEY)
    failure = get_value_num(FAILURE_KEY)
    rates = get_range_num(RATES)

    print('-' * 15 + name + '-' * 15)
    print("Stats")
    print("Concurrent Level:      ", processes, 'X', threads )
    print("Success                ", success)
    print("Failure                ", failure)
    print("Qps                    ", pre)
    count  = collections.Counter(rates)
    for c in count:
        print(" {:>4.0%}      ".format(c), count[c])


class SimpleTest(BaseQuery):

    def check_a(self):
        return True

    def check_b(self):
        return False

class TestFalsk(BaseQuery):
    """Simple test"""
    def __init__(self):
        super().__init__()
        self.url = 'http://127.0.0.1:8000'

    def check_get(self):
        return self.session.get(self.url).status_code == 200

    def check_post(self):
        data = {
            'data': 'test',
        }
        return self.session.post(self.url+'/post', data=data).status_code == 200


def main(process, threads, task, times=2048):
    allcost = work(task, process, threads, times=times)
    pre = round(times // allcost, 2)
    report(process, threads, task.__name__, pre)


if __name__ == '__main__':
    main(2, 16, TestFalsk, 4096)
