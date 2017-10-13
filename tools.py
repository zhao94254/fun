# 常用的工具函数
import time
from functools import wraps
import inspect
import sys
import logging

def timeit(func):
    """统计函数运行时间"""
    t0 = time.perf_counter()
    func()
    return time.perf_counter() - t0


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
    """跟踪函数，便于查看过程。"""
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




