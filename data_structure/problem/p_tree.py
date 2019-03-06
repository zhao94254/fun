#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 17/11/17 下午4:51
# @Author  : zpy
# @Software: PyCharm

from datastructre.tree import BinTree

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

def preorder(root):
    res = []
    def preorderTraversal(root):
        """先序遍历"""
        if root is None:
            return None
        res.append(root.val)
        preorderTraversal(root.left)
        preorderTraversal(root.right)
        return res
    preorderTraversal(root)
    return res


def preorderTraversal2(root):
    """
    先序 使用不使用递归，思路就是通过栈来。
    和bfs的区别是 每次弹出栈顶。要先压入right。这样子才可以先拿到左
    :param root:
    :return:
    """
    res = []
    if root:
        stack = [root]
        while len(stack) > 0:
            cur = stack.pop()
            res.append(cur.val)
            if cur.right:
                stack.append(cur.right)
            if cur.left:
                stack.append(cur.left)
    return res


def midorder(root):
    """
    中序非递归，思路 把所有的左子树全部压入，
    然后压入右子树，压入
    :param root:
    :return:
    """
    res = []
    if root:
        stack = []
        while len(stack) > 0 or root:
            if root:
                stack.append(root)
                root = root.left
            else:
                root = stack.pop()
                res.append(root.val)
                root = root.right
    return res


def inorder(root):
    """
    后序非递归。按照根右左的 顺序压入。每次都在头节点加入
    :param root:
    :return:
    """
    s1 = [root]
    s2 = []
    while len(s1) > 0:
        cur = s1.pop()
        s2.insert(0, cur.val)
        if cur.left:
            s1.append(cur.left)
        if cur.right:
            s1.append(cur.right)
    return s2


def invert_tree(root):
    """翻转二叉树"""
    if root is None:
        return None
    root.right, root.left = root.left, root.right
    invert_tree(root.left)
    invert_tree(root.right)
    return root


def tree_height(root):
    """返回树的高度"""
    if root is None:
        return 0
    return max(tree_height(root.left), tree_height(root.right)) + 1


def tree_height_min(root):
    """树的最小高度"""
    def help(root):
        if root is None:
            return 0
        if root.left is None and root.right is None:
            return 1
        return min(help(root.left), help(root.right)) + 1

    return help(root)


def tree_identical(a, b):
    """判断两个二叉树是否相等"""
    if a is None and b is None:
        return True
    if not (a and b):
        return False
    if a.val == b.val:
        return tree_identical(a.left, b.left) and tree_identical(a.right, b.right)
    else:
        return False


def is_subtree(a, b):
    """检查a 是否是 b 的子树"""
    def help(a, b):
        if a is None or b is None:
            return a == b
        if a.val != b.val:
            return False
        return help(a.left, b.left) and help(a.right, b.right)

    if a is None:
        return False
    if b is None:
        return True
    if help(a, b):
        return True

    if is_subtree(a.left, b) or is_subtree(a.right, b):
        return True
    return False


def lowest_ancestor(root, A, B):
    """
    最近公共祖先。思路，通过遍历递归，往出退出递归栈时查看是否满足了条件。
    :param root:
    :param A:
    :param B:
    :return:
    """
    if root is None:
        return None
    if root.val == A or root.val == B:
        return True

    left = lowest_ancestor(root.left, A, B)
    right = lowest_ancestor(root.right, A, B)

    if left and right:
        return root.val
    if left:
        return left
    if right:
        return right
    return None


def showtree(tree, indent=0):
    """先序"""
    if tree is None:
        return ''
    else:
        print(indent * ' ' + str(tree.val))
        showtree(tree.left, indent + 1)
        showtree(tree.right, indent + 1)


def inver(tree):
    """ 二叉树反转 函数式写法"""
    if tree is None:
        return tree
    return BinTree(tree.val, inver(tree.right), inver(tree.left))


def getleft(tree):
    """获得树最左边的元素"""
    if tree.left is None:
        return None
    print(tree.left.val)
    getleft(tree.left)