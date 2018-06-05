#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/3/2 下午7:02
# @Author  : zpy
# @Software: PyCharm


from collections import namedtuple
import copy
import csv

def create_table(row, data):
    """row[0] 表名  row[1:] 列名 data 要插入的数据"""
    table_row = namedtuple(row[0], row[1:])
    table = [table_row(*i) for i in data]
    return table

def table_to_dict(table):
    """ namedtuple -> dict"""
    res = []
    for t in table:
        res.append({field: getattr(t, field) for field in t._fields})
    return res

def filter(condition, row):
    """ 按照要求的条件进行过滤"""
    if condition:
        return eval(condition, row)
    else:
        return True

def split_name(name):
    """ xx, yy,zz -> [xx, yy, zz]"""
    return sum([i.split() for i in name.split(',')], [])

def get_data(name, row):
    """ 获取row中的多个值"""
    #print(row.values())
    if not isinstance(name, (list, tuple)):
        name = [name]
    data = [row[i] for i in name]
    return data[0] if len(data) == 1 else data

def group_get_datas(names, row):
    if isinstance(names, list):
        return [group_get_data(i, row) for i in names]
    else:
        return group_get_data(names, row)

def group_get_data(name, row):
    if name.startswith('count('):
        return len(row)
    elif name.startswith('sum('):
        t_name = name[4:-1]
        return sum([get_data(t_name, r) for r in row])
    else:
        return row[0][name]

def select(name, table, condition=None, group_by=None):
    """ select name from table where condition"""
    res = []
    tmp = {}
    if name == '*':
        name = table[0]._fields
    else:
        name = split_name(name)
    for j, i in enumerate(table_to_dict(table)):
        if condition is None or filter(condition, i): # 第一步，首先进行过滤
            if group_by:
                first_key = get_data(group_by, i) # 这里进行 count， sum 等操作
                if first_key in tmp:
                    tmp[first_key].append(i)
                else:
                    tmp[first_key] = [i]
            else:
                res.append(get_data(name, i))
    if tmp:
        res = []
        for i, j in tmp.items():
            res.append(group_get_datas(name, j))
        return res

    return res[0] if len(res) == 1 else res

def unname(lst):
    """ 会有一些 Unnamed: xx 的，要变成 --> NULLxx"""
    for i, j in enumerate(lst):
        if j.startswith('Unnamed'):
            lst[i] = "NULL" + lst[i].split(':')[-1][1:]


def read_csv(filename):
    """ 将csv 文件加入，进行一些过滤"""
    data = []
    with open(filename) as f:
        f_csv = csv.reader(f)
        row = ["Row"] + next(f_csv)
        unname(row)
        for i, d in enumerate(f_csv):
            data.append(d)
            if i == 10:
                break

    return create_table(row, data)

if __name__ == '__main__':
    import random
    import pprint

    row = ('Row', 'name', 'age', 'location', 'money')
    data = [('jack', 12, 'beijing', 15),
            ('rose', 15, 'shanghai', 23),
            ('aha', 20, 'taiyuan', 345),
            ('liuxing', 18, 'changzhi', 432),
            ('luben', 18, 'shanghai', 233),
            ('douchuan', 18, 'changzhi', 322),
            ('heihai', 18, 'shanghai', 199),]
    table = create_table(row, data)
    # print(select('name', table, "name == 'luben'"))
    # print(select('name, age', table, "name != 'luben'"))
    print(select('*', table, "age >= 11  and location=='beijing'"))
    print(select('location, sum(money)', table, "age>=18", 'location'))
