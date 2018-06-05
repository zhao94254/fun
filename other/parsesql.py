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
    if not isinstance(name, list):
        name = [name]
    data = [row[i] for i in name]
    return data[0] if len(data) == 1 else data

def select(name, table, condition=None, group_by=None):
    """ select name from table where condition"""
    res = []
    tmp = {}
    if name == '*':
        name = table[0]._fields
    else:
        name = split_name(name)
    for j, i in enumerate(table_to_dict(table)):
        if condition is None or filter(condition, i):
            res.append(get_data(name, i))
        if group_by:
            first_key = get_data(group_by, i)
            if first_key in tmp:
                tmp[first_key].append(get_data(name, i))
            else:
                tmp[first_key] = [get_data(name, i)]
    if tmp:
        return tmp.keys(), tmp.items()
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

    row = ('Row', 'name', 'age', 'location')
    data = [('jack', 12, 'beijing'),
            ('rose', 15, 'shanghai'),
            ('aha', 20, 'taiyuan'),
            ('liuxing', 18, 'changzhi'),
            ('luben', 18, 'shanghai'),
            ('douchuan', 18, 'changzhi'),
            ('heihai', 18, 'shanghai'),]
    table = create_table(row, data)
    # print(select('name', table, "name == 'luben'"))
    # print(select('name, age', table, "name != 'luben'"))
    # print(select('*', table, "age >= 18 and location=='changzhi'"))
    print(select('name', table, "age>=18", 'location'))
