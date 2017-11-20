#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:51
# @Author  : zpy
# @Software: PyCharm

from ..data_structre.tree import BinTree


def is_symmetrical(tree1, tree2):
    """检查两个树是否互为镜像树"""
    def helper(l, r):
        if l is None and r is None:
            return True
        if l is None or r is None:
            return False
        if l.val != r.val:
            return False
        return helper(l.left, r.right) and helper(l.right, r.left)
    if tree1 is None and tree2 is None:
        return True
    return helper(tree1.left, tree2.right)