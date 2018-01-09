#!/usr/bin/env python
# @Author  : pengyun

# 二叉树抽象

class BinTree:
    """
    二叉树。
    使用__call__方法进行序列化，将列表直接转化为一个树
    >>> ctree = BinTree()
    >>> tree = ctree([1,2,3,4,5,6,7,8,9,10])
    >>> tree
    [1]
    [2, 3]
    [4, 5, 6, 7]
    [8, 9, 10]
    this is tree
    """

    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

    def __str__(self):
        return self.print_tree()

    __repr__ = __str__

    def __call__(self, *args):
        return self.list_to_tree(*args)

    def list_to_tree(self, data):
        """
        list --> tree
        # 代表空节点
        :param data:
        :return:
        """
        root = BinTree(data[0])
        queue = [root]
        isleft = True
        index = 0
        for val in data[1:]:
            if val != '#':
                node = BinTree(val)
                if isleft:
                    queue[index].left = node
                else:
                    queue[index].right = node
                queue.append(node)
            if not isleft:
                index += 1
            isleft = not isleft
        return root

    def preorder(self, root, level, res):
        """将树的每一层分开"""
        if root:
            if len(res) < level + 1: res.append([])
            res[level].append(root.val)
            self.preorder(root.left, level + 1, res)
            self.preorder(root.right, level + 1, res)

    def print_tree(self):
        res = self.levelorder(self)
        for i in res:
            print(i)
        return 'this is tree'

    def levelorder(self, root):
        """调用分层的方法，返回分层的树"""
        res = []
        self.preorder(root, 0, res)
        return res

    def bfs(self, root):
        """宽度优先遍历"""
        _res = []
        q = [root]
        while len(q) > 0:
            tmp = q.pop(0)
            _res.append(tmp.val)
            if tmp.left:
                q.append(tmp.left)
            if tmp.right:
                q.append(tmp.right)
        return _res

    def convert_to_bst(self, data):
        """有序列表转化成二叉搜索树"""

        def build(data, start, end):
            """和二分搜索差不多， 递归创建"""
            if start > end:
                return None
            tree = BinTree(data[(start + end) // 2])
            tree.left = build(data, start, (start + end) // 2 - 1)
            tree.right = build(data, (start + end) // 2 + 1, end)
            return tree

        if len(data) == 0:
            return None
        return build(data, 0, len(data) - 1)




if __name__ == '__main__':
    ctree = BinTree(0)
    tree = ctree(list(range(10)))


    btree = tree([1, '#', 2, 3, 4])

    print(tree)

