#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 18/3/2 下午7:02
# @Author  : zpy
# @Software: PyCharm


from collections import namedtuple


def create_table(row, data):
    table_row = namedtuple(row[0], row[1:])
    table = [table_row(*i) for i in data]
    return table


if __name__ == '__main__':
    row = ('test', 'name', 'age')
    data = [('jakc', 12), ('rose', 18)]
    print(create_table(row, data))




