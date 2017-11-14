#!/usr/bin/env python
# @Author  : pengyun

# pythonic & one line








# 丧心病狂的一行代码实现。

# python3 -m http.server port 一行开启web服务。
# 如果是需要分享一些东西这个功能简直不能太赞

# 如果是复杂的 无法一眼读下来的代码是不应该在程序中追求这种写法的
# from operator import sub, mul
# fact = lambda n : 1 if n == 1 else mul(fact(n-1), n) 一行求阶乘
# fib = lambda n : n if n < 2 else fib(n-1) + fib(n-2) 一行求fib

# 一行9 9乘法表
# print('\n'.join([ ' '.join([ "{}*{}={}".format(i, j, i*j)for j in range(1, i+1)]) for i in range(1, 10)]))

# 一行把 多维数组变为一维\
# flatten = lambda x: [i for j in x for i in flatten(j)] if isinstance(x, list) else [x]

# 一行筛素数
# prime = lambda n: [ i for i in range(2, n) if all([i%j!=0 for j in range(2, i)])]
# prime = lambda n: [ i for i in range(2, n) if all(map(lambda j: i%j!=0, range(2, i)))]

# 强行一行二分搜索
bs = lambda x, y, i, j: None if i > j else y == x[(i+j)//2] \
                                            or (y < x[(i+j)//2] and bs(x, y, i, (i+j)//2-1)) \
                                            or (y > x[(i+j)//2] and bs(x, y, (i+j)//2+1, j))

# print(bs((4,6,10,12,20,30,50,70,88,100),2,0,9))