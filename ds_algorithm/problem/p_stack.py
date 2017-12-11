#!/usr/bin/env python
# @Author  : pengyun


class MinStack:
    """
    带最小值的栈。思路 使用一个数组来保存最小的数。
    """

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, data):
        self.stack.append(data)
        if not self.min_stack or data <= self.min_stack[-1]:
            self.min_stack.append(data)

    def pop(self):
        if self.stack[-1] == self.min_stack[-1]:
            self.stack.pop()
            return self.min_stack.pop()
        return self.stack.pop()

    def min(self):
        return self.min_stack[-1]


def deltag(s):
    """ 去除标签 <asdf>阿斯顿付款了<asdf> -->阿斯顿付款了"""
    res = []
    stack = []
    for i in s:
        if i == "<":
            stack.append(i)  # 标记是否处于标签内
        elif i == ">":
            if len(stack) > 0:
                stack.pop()
        else:
            if len(stack) > 0:  # 处于
                pass
            else:
                res.append(i)
    return "".join(res)


def valid_parentheses(s):
    """有效的括号序列"""
    stack = []
    for i in s:
        if i == '(':
            stack.append(i)
        elif i == ')' and len(stack) == 0:
            return False
        else:
            stack.pop()
    return True


def eval_rpn(lst):
    """逆波兰求值"""
    stack = []
    for i in lst:
        if i == '+':
            a1, a2 = stack.pop(), stack.pop()
            stack.append(a1 + a2)
        elif i == '-':
            a1, a2 = stack.pop(), stack.pop()
            stack.append(a2 - a1)
        elif i == '*':
            a1, a2 = stack.pop(), stack.pop()
            stack.append(a2 * a1)
        elif i == '/':
            a1, a2 = stack.pop(), stack.pop()
            stack.append(int(a2 / a1))
        else:
            stack.append(int(i))
    return stack[-1]


def join_s(s):
    tmp = ''
    res = []
    for i in s:
        if isinstance(i, int) or i in '[]':
            if tmp:
                res.append(tmp)
                tmp = ''
            res.append(i)
        else:
            tmp += i
    return res


def find132(s):
    """
    判断s中是否有 s[1]<s[3]<s[2]的
    思路 通过两个栈来保存，一个保存每个位置最小的值，一个用来放比当前位置大的值。
    将第二大的数从maxstack中间弹出来，和minstack中放的当前位置的进行对比，如果满足
    返回True
    """
    minstack = [0] * len(s)
    maxstack = []
    minstack[0] = s[0]
    for i in range(1, len(s)):  # 拿到每个位置的最小值
        minstack[i] = min(minstack[i - 1], s[i])

    for j in range(len(s) - 1, 0, -1):
        m = -1111
        while len(maxstack) > 0 and maxstack[-1] < s[j]:
            m = maxstack.pop()  # 弹出第二大的
        maxstack.append(s[j])
        if minstack[j - 1] < m:  # 要么弹出来第二大的数，要么就是默认的极小值，如果
            return True  # 比之前位置的数都小就返回True
    return False


def popstack(s):
    """获取s这个栈中的一段字符"""
    res = ''
    while len(s) > 0 and not isinstance(s[-1], int):
        t = s.pop()
        res += t
    return res


def split_express(s):
    """将多位数字分开
    >>>print(split_express("3[2[ad]3[pf]]1[xyz]"))
    [3, '[', 2, '[', 'a', 'd', ']', 3, '[', 'p', 'f', ']', ']', 1, '[', 'x', 'y', 'z', ']']
    """
    res = []
    tmp = ''
    for i in s:
        if i in '1234567890':
            tmp += i
        else:
            if tmp:
                res.append(int(tmp))
                tmp = ''
            res.append(i)
    return res


def expressionExpand(s):
    """
    这个主要考栈的使用，和字符串的处理。将这个问题拆成多个函数来解决问题
    就简单很多。通过一个popstack函数来获取一段字符，通过判断是否是] 来决定
    是否需要进行计算。
    >>>expressionExpand(3[abc])
    abcabcabc

    """
    stack = []
    s = split_express(s)
    for i in s:
        if i == "[":
            pass
        elif i == ']':
            t = popstack(stack)
            c = stack.pop()
            stack.append(t * c)
        else:
            stack.append(i)
    for i in range(len(stack)):
        stack[i] = stack[i][::-1]
    return "".join(stack)


if __name__ == '__main__':
    print(valid_parentheses('(()()((()))'))
    print(eval_rpn(
        ["-78", "-33", "196", "+", "-19", "-", "115", "+", "-", "-99", "/", "-18", "8", "*", "-86", "-", "-", "16", "/",
         "26", "-14",
         "-", "-", "47", "-", "101", "-", "163", "*", "143", "-", "0", "-", "171", "+", "120", "*", "-60", "+", "156",
         "/", "173", "/", "-24",
         "11", "+", "21", "/", "*", "44", "*", "180", "70", "-40", "-", "*", "86", "132", "-84", "+", "*", "-", "38",
         "/", "/", "21", "28", "/", "+",
         "83", "/", "-31", "156", "-", "+", "28", "/", "95", "-", "120", "+", "8", "*", "90", "-", "-94", "*", "-73",
         "/", "-62", "/", "93", "*", "196", "-", "-59", "+", "187", "-", "143", "/", "-79", "-89", "+", "-"]))
    print(expressionExpand("3[abc]"))
