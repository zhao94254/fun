from turtle import *
import argparse


class Block(Turtle):
    def __init__(self, size):
        Turtle.__init__(self, shape="square", visible=False)
        self.size = size
        self.up() # penup
        self.shapesize(size * 2, 1, 1) # square-->rectangle
        self.fillcolor("black")
        self.st() # showturtle

    def glow(self):
        self.fillcolor("red")

    def unglow(self):
        self.fillcolor("black")

    def __repr__(self):
        return "Block size: {0}".format(self.size)


class Shelf(list):
    def __init__(self, x, y):
        "创建起始坐标"
        self.x = x
        self.y = y

    def push(self, b):
        width, _, _ = b.shapesize()
        # 对齐底部
        y_offset = width / 2 * 20
        b.sety(self.y + y_offset)
        b.setx(self.x + 34 * len(self))
        self.append(b)

    def move_left(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos - 34)

    def move_right(self, i):
        for b in self[i:]:
            xpos, _ = b.pos()
            b.setx(xpos + 34)

    def pop(self, key):
        """设置弹出的效果，"""
        b = list.pop(self, key)
        b.glow()
        b.sety(200)
        self.move_left(key)
        return b

    def insert(self, key, b):
        self.move_right(key)
        list.insert(self, key, b)
        b.setx(self.x + 34 * key)
        width, _, _ = b.shapesize()
        # 对齐底部
        y_offset = width / 2 * 20
        b.sety(self.y + y_offset)
        b.unglow()


def init_block():
    s = Shelf(-150, -200)
    for i in (4, 2, 8, 9, 1, 5, 10, 3, 7, 6):
        s.push(Block(i))
    return s


def bubble_sort(data):
    lens = len(data)
    for i in range(lens):
        for j in range(i):
            if data[i].size < data[j].size:
                data.insert(j, data.pop(i))


def select_sort(data):
    _len = len(data)
    for i in range(_len):
        _min = i
        for j in range(i + 1, _len):
            if data[j].size < data[_min].size:
                _min = j
        if _min != i:
            data.insert(i, data.pop(_min))


def partition(data, left, right):
    pivot = data[right]
    wall = left
    for i in range(left, right):
        if data[i].size < pivot.size:
            data.insert(wall, data.pop(i))
            wall += 1
    data.insert(wall, data.pop(right))
    return wall


def qsort(data, left, right):
    if left < right:
        newpivot = partition(data, left, right)
        qsort(data, left, newpivot - 1)
        qsort(data, newpivot + 1, right)


def quick_sort(data):
    return qsort(data, 0, len(data)-1)


def insert_sort(data):
    for i in range(1, len(data)):
        for j in range(i, 0, -1):
            if data[j].size < data[j-1].size:
                data.insert(j, data.pop(j-1))


def main():
    data = init_block()
    _map = {
        'b': bubble_sort,
        's': select_sort,
        'q': quick_sort,
        'i': insert_sort,
    }
    parser = argparse.ArgumentParser(description="Run \r\n b--Bubble sort \
                                                     s--Select sort\
                                                     q--Quick sort \
                                                     i--Insert sort")

    parser.add_argument("-v", '--version', dest="method", default=False)
    args = parser.parse_args()
    print(_map[args.method].__name__)
    _map[args.method](data)

if __name__ == '__main__':
    main()





