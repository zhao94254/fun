# 常用的工具函数
import time
from functools import wraps
import inspect
import sys
import logging
import signal
import code
import os

try:
    import Mysqldb as pymysql
except ImportError:
    import pymysql

class Mysql:
    def __init__(self, stream=False, **kw): #  MySQLdb.cursors.SSCursor 流式游标
        if stream == True:
            self._connect = pymysql.connect(cursorclass = pymysql.cursors.SSCursor, **kw)
        else:
            self._connect = pymysql.connect(**kw)
    def __enter__(self):

        cursor = self._connect.cursor()
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._connect.commit()

        self._connect.close()

def getfile(path, end=None):
    """获取指定路径下的所有文件"""
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

def retry(times=3):
    """对一个函数进行重试"""
    def wrap(func):
        def do(*args, **kwargs):
            t = times
            res = None
            while t > 0:
                try:
                    res = func(*args, **kwargs)
                    break
                except Exception:
                    t -= 1
            return res
        return do
    return wrap


def timeit(func):
    """精确统计函数运行时间"""
    t0 = time.perf_counter()
    func()
    return time.perf_counter() - t0

def count_func_time(func):
    """统计函数运行时间的装饰器"""
    def inner(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print("function: {} -- cost time".format(func.__name__), time.time() - start)
        return res
    return inner

def count_func_timeit(func):
    """精确统计函数运行时间的装饰器"""
    def inner(*args, **kwargs):
        start = time.perf_counter()
        res = func(*args, **kwargs)
        print("function: {} -- cost time".format(func.__name__), time.perf_counter() - start)
        return res
    return inner

def count(func):
    """统计递归函数执行次数"""
    # @wraps(func)
    def counted(*args):
        counted.call_count += 1
        return func(*args)
    counted.call_count = 0
    return counted


def memorize(f):
    """缓存"""
    cache = {}
    @wraps(f)
    def memorized(*args):
        if args not in cache:
            cache[args] = f(*args)
        return cache[args]
    return memorized


class CacheProperty:
    """对于一个实例只计算一次。保存在实例字典中"""
    def __init__(self, func):
        self.func = func
        self.__doc__ = getattr(func, '__doc__')

    def __get__(self, instance, owner):
        if instance is None:
            return self
        else:
            value = instance.__dict__[self.func.__name__] = self.func(instance)
            # value = self.func(instance)
            # setattr(instance, self.func.__name__, value)
            return value


def trace(func):
    """跟踪函数，便于查看函数执行过程。"""
    def afunc(*args):
        print("call", func.__name__, "with", args)
        v = func(*args)
        print(func.__name__, "return ",v)
        return v
    return afunc


def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        @wraps(func)
        def wrapper(*args, **kwargs):
            logmsg = "{}--call --{}".format(func.__name__, args)
            log.log(level, logmsg)
            return func(*args, **kwargs)
        return wrapper
    return decorate


def main(fn):
    """@main ---> __name__ == "__main__" """
    if inspect.stack()[1][0].f_locals['__name__'] == '__main__':
        args = sys.argv[1:] # Discard the script name from command line
        fn(*args) # Call the main function
    return fn


# 例子
# 统计调用次数 增加缓存 增加debug 功能。
@logged(logging.DEBUG)
@count
@memorize
def fib(x):
    return x if x < 2 else fib(x-1) + fib(x-2)


def interact(msg=None):
    """类似于 pdb.stace() 的函数

    On Unix:
      <Control>-D exits the interactive session and returns to normal execution.
    In Windows:
      <Control>-Z <Enter> exits the interactive session and returns to normal
      execution.
    """
    # evaluate commands in current namespace
    frame = inspect.currentframe().f_back
    namespace = frame.f_globals.copy()
    namespace.update(frame.f_locals)

    # exit on interrupt
    def handler(signum, frame):
        print()
        exit(0)
    signal.signal(signal.SIGINT, handler)

    if not msg:
        _, filename, line, _, _, _ = inspect.stack()[1]
        msg = 'Interacting at File "{0}", line {1} \n'.format(filename, line)
        msg += '    Unix:    <Control>-D continues the program; \n'
        msg += '    Windows: <Control>-Z <Enter> continues the program; \n'
        msg += '    exit() or <Control>-C exits the program'

    code.interact(msg, None, namespace)


# # python2
# def table_to_csv(filepath):
#     f = file(filepath)
#     html_content = f.read()
#     soup = BeautifulSoup(html_content)
#     table = soup.select_one("table")
#     for row in table.select("tr"):
#         print [r.text.encode("utf-8") for r in row.select("td")]

# python3
from bs4 import BeautifulSoup
def table_to_csv(filepath):
    with open(filepath) as f:
        html_content = f.read()
        soup = BeautifulSoup(html_content)
        table = soup.select_one("table")
        for row in table.select("tr"):
            print([r.text for r in row.select("td")])

def xls_to_csv(filename):
    """ xls 转为 csv 文件"""
    import pandas
    name = filename.split('.')[-2]
    xls = pandas.read_excel(filename, index_col=None)
    xls.to_csv('{}.csv'.format(name), encoding='utf-8')

def sum_dict(a, b):
    """
    将两个字典reduce 起来，支持嵌套的dict
    :param a: {'adult': {'zero': 0}, 'price': {'other': 347748, '-1': 9}, 'rest': {'-1': 336707}, 'hotelname': {'min3': 18, 'NULL': 26, 'all_string': 29615}, 'bed': {'other': 336716, 'NULL': 11041}, 'desc': {'fivelen': 9053, 'other': 337730, 'NULL': 974}, 'size': {'min10': 9739, 'other': 322761, '-1': 15257}}
    :param b: {'adult': {'zero': 0}, 'price': {'other': 347748, '-1': 9}, 'rest': {'-1': 336707}, 'hotelname': {'min3': 18, 'NULL': 26, 'all_string': 29615}, 'bed': {'other': 336716, 'NULL': 11041}, 'desc': {'fivelen': 9053, 'other': 337730, 'NULL': 974}, 'size': {'min10': 9739, 'other': 322761, '-1': 15257}}
    :return:  # {'adult': {'zero': 0}, 'price': {'other': 695496, '-1': 18}, 'rest': {'-1': 673414}, 'hotelname': {'min3': 36, 'NULL': 52, 'all_string': 59230}, 'bed': {'other': 673432, 'NULL': 22082}, 'desc': {'fivelen': 18106, 'other': 675460, 'NULL': 1948}, 'size': {'min10': 19478, 'other': 645522, '-1': 30514}}, {'adult': {'zero': 0}, 'price': {'other': 347748, '-1': 9}, 'rest': {'-1': 336707}, 'hotelname': {'min3': 18, 'NULL': 26, 'all_string': 29615}, 'bed': {'other': 336716, 'NULL': 11041}, 'desc': {'fivelen': 9053, 'other': 337730, 'NULL': 974}, 'size': {'min10': 9739, 'other': 322761, '-1': 15257}}
    """
    def helper(a, b):
        for k in a.keys():
            # 如果k 不在b里，添加默认的
            if k not in b:
                if isinstance(a[k], dict):
                    b[k] = {}
                else:
                    b[k] = 0
            if isinstance(a[k], dict):
                helper(a[k], b[k])
            else:
                a[k] += b[k]
        return a
    return helper(a, b)
