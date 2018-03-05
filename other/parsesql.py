#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/3/2 下午7:02
# @Author  : zpy
# @Software: PyCharm


from collections import namedtuple
import copy

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
    data = [row[i] for i in name]
    return data[0] if len(data) == 1 else data

def select(name, table, condition):
    """ select name from table where condition"""
    res = []
    if name == '*':
        name = table[0]._fields
    else:
        name = split_name(name)
    for j, i in enumerate(table_to_dict(table)):
        if filter(condition, i):
            res.append(get_data(name, i))
    return res[0] if len(res) == 1 else res

if __name__ == '__main__':
    import random

    row = ('Row', 'name', 'age', 'location')
    data = [('jack', 12, 'beijing'),
            ('rose', 15, 'shanghai'),
            ('aha', 20, 'taiyuan'),
            ('liuxing', 18, 'changzhi'),
            ('luben', 18, 'shanghai'),
            ('douchuan', 18, 'changzhi'),
            ('heihai', 18, 'shanghai'),]
    table = create_table(row, data)
    print(select('name', table, "name == 'luben'"))
    print(select('name, age', table, "name != 'luben'"))
    print(select('*', table, "age >= 18 and location=='changzhi'"))

