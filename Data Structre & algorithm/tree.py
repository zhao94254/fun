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


def preorderTraversal(root):
    """先序遍历"""
    if root is None:
        return None
    res.append(root.val)
    preorderTraversal(root.left)
    preorderTraversal(root.right)
    return res


def preorderTraversal_(root):
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
    if tree is None:
        return tree
    return BinTree(tree.val, inver(tree.right), inver(tree.left))


def getleft(tree):
    if tree.left is None:
        return None
    print(tree.left.val)
    getleft(tree.left)


if __name__ == '__main__':
    ctree = BinTree(0)
    tree = ctree(list(range(10)))
    getleft(tree)

    showtree(tree)
    showtree(inver(tree))

    btree = tree([1, '#', 2, 3, 4])

    print(tree)
    print(lowest_ancestor(tree, 7, 8))
    print(invert_tree(btree))
    print(preorderTraversal(root=btree))
    print(preorderTraversal_(btree))
    print(midorder(btree))
    print(inorder(btree))

    print(tree_height(btree))
    print(tree_height_min(btree))
    print(tree_identical(btree, btree))
