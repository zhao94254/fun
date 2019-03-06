#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/12/11 下午6:40
# @Author  : zpy
# @Software: PyCharm


from units import getfunc
import argparse
import os


def main():
    parser = argparse.ArgumentParser(description="Run \r\n -f find function or class"
                                                 )
    parser.add_argument("-f", '--find', dest="name", default=False)
    args = parser.parse_args()
    getfunc(os.getcwd(), args.name)





if __name__ == '__main__':
    main()
    #getfunc('/Users/mioji/Desktop/py/github/fun/ds_algorithm', '背包')









