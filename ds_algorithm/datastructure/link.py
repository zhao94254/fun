#!/usr/bin/env python
# @Author  : pengyun

# 链表抽象
# 和数组相比主要的缺点是查找一个元素麻烦

class Linklist:
    def __init__(self, x=None, next=None):
        self.val = x
        self.next = next

    def __str__(self):
        return "{}-->{}".format(self.val, self.next)

    __repr__ = __str__

    def __len__(self):
        if self.next is None:
            return 1
        return 1 + len(self.next)

    def __getitem__(self, i):
        if self.next is None:
            return None
        if i == 0:
            return None
        else:
            return self.next[i - 1]

    def __call__(self, x: list):
        return self.list_to_link(x)

    def list_to_link(self, x: list):
        """将数组转化为链表"""
        head = Linklist(0)
        cur = head
        for i in x:
            if isinstance(i, Linklist):
                cur.next = i
            else:
                cur.next = Linklist(i)
            cur = cur.next
        return head.next


def map_link(f:'function', s: 'str'):
    if s is None:
        return s
    else:
        return Linklist(f(s.val), map_link(f, s.next))


def filter_link(f:'function', s:'str'):
    if s is None:
        return s
    else:
        filtered = filter_link(f, s.next)
        if f(s.val):
            return Linklist(s.val, filtered)
        else:
            return filtered


def extend_link(s:'link', t:'link'):
    if s is None:
        return None
    else:
        return Linklist(s.val, extend_link(s.next, t))


def join_link(s, separator=", "):
    if s is None:
        return ""
    elif s.next is None:
        return str(s.val)
    else:
        return str(s.val) + separator + join_link(s.next, separator)


def partitions(n, m):
    if n == 0:
        return Linklist()
    elif n < 0 or m == 0:
        return None
    else:
        using_m = partitions(n - m, m)
        with_m = map_link(lambda x: Linklist(m, x), using_m)
        without_m = partitions(n, m - 1)
        # print(with_m, without_m)
        return extend_link(with_m, without_m)


def add_two_numbers(left: "Linklist", right: "Linklist"):
    head = Linklist(0)
    cur = head
    _sum = 0
    while left or right:
        _sum //= 10
        if left:
            _sum += left.val
            left = left.next
        if right:
            _sum += right.val
            right = right.next
        cur.next = Linklist(_sum % 10)
        cur = cur.next
    if _sum // 10 == 1:
        cur.next = Linklist(1)
    return head.next


def remove(x: "link", y: "int"):
    """删除指定节点"""
    head = Linklist(0)
    head.next = x
    cur = head
    while cur.next:
        if cur.next.val == y:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head.next


def reverse(x: "link"):
    """链表逆序 保存next 指向前面节点， 断开链表 res指向断开这里"""
    res = None
    while x:
        rest = x.next
        x.next = res
        res = x
        x = rest
    return res


def merge_two_link(a, b):
    head = Linklist(0)
    cur = head
    while a and b:
        if a.val <= b.val:
            cur.next = a
            a = a.next
        else:
            cur.next = b
            b = b.next
        cur = cur.next
    if a:
        cur.next = a
    if b:
        cur.next = b
    return head.next


def rotate_list(link, x):
    """从x的位置分割开"""
    cur = link
    while x > 0:
        x -= 1
        cur = cur.next
    next = cur.next
    cur.next = None
    return next, link


def swapPairs(head):
    pre = Linklist(0)
    move = pre
    move.next = head

    while move.next and move.next.next:
        a = move.next
        b = move.next.next
        # 当前的是move.next  这个指向下一个，下一个回指回来 a再指向下下个
        move.next, a.next, b.next = b, b.next, a
        move = a
    return pre.next


def cycle(node):
    """获取产生循环的那一段"""
    slow, fast = node, node.next
    while slow != fast:
        if fast is None or fast.next is None:
            return None
        slow = slow.next
        fast = fast.next.next
    slow = node
    fast = fast.next
    while slow != fast:
        slow = slow.next
        fast = fast.next
    return slow


def getIntersction(node1, node2):
    """其实是一个变相判断循环的问题 如果两个节点都有一段C 然后C再指向后面的，造成循环"""
    if node1 is None or node2 is None:
        return None
    head = node1
    while head.next:
        head = head.next
    head.next = node2
    res = cycle(node1)
    # 将后面的断开
    head.next = None
    return res


def is_cycle(x):
    a, b = x, x
    while x:
        a = a.next.next
        b = b.next
        if a == b:
            return True
        if a is None or b is None:
            return False
    return False


def map_link(fn, link):
    if link is None:
        return None
    return Linklist(fn(link.val), map_link(fn, link.next))


def list_to_link(x: list):
    """将数组转化为链表"""
    head = Linklist(0)
    cur = head
    for i in x:
        if isinstance(i, Linklist):
            cur.next = i
        else:
            cur.next = Linklist(i)
        cur = cur.next
    return head.next


def reverse1(link):
    # 使用了额外的空间
    res = Linklist(link.val)
    while link.next:
        link = link.next
        res = Linklist(link.val, res)

    return res

def insert_sort(link):
    """思路就是 先将链表制空，然后保存当前的"""
    h = Linklist(0) # 头节点
    while link:
        tmp = h # 工作指针
        _n = link.next # 保存当前待排序节点
        while tmp.next and tmp.next.val < link.val: # 确保tmp中的都是比当前待排序节点大的
            tmp = tmp.next
        link.next = tmp.next # 将当前节点增加到已排序的tmp中
        tmp.next = link # tmp增加
        link = _n # 指回待排序节点
    return h.next

if __name__ == '__main__':
    a = list_to_link([9, 9, 9])
    b = list_to_link([3, 1, 5, 4, 66, 12, 14])
    print(reverse1(b))
    print(merge_two_link(a, b))
    print(remove(a, 1))
    print(reverse(a))
    print(map_link(lambda x: x * x, a))
    print(add_two_numbers(a, b))

    a = list_to_link([1,3,4,5,6,7])
    print(rotate_list(a, 2))
    print(a, b)
    print(getIntersction(a, b))
    square = lambda x: x * x
    odd = lambda x: x % 2
    x = list(range(10))
    a = Linklist()
    link = a(x)
    print(link)
    print(filter_link(odd, link))
    print(join_link(link))
    print(partitions(6, 4))
