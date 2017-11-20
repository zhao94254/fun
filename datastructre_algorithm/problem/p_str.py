#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:51
# @Author  : zpy
# @Software: PyCharm




def is_rotate(s1, s2):
    """
    >>>is_rotate('12345', '34512')
    True
    :param s1:
    :param s2:
    :return:
    """
    if s2 in s1*2:
        return True
    return False
