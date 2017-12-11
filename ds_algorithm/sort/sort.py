import time
import argparse


def log(data: list, sleep: float):
    print("\r" + ''.join(data), end='', flush=True)
    time.sleep(sleep)


def bubble_sort(data):
    for i in range(len(data)):
        for j in range(i):
            if data[i] < data[j]:
                data[i], data[j] = data[j], data[i]
            log(data, speed)
    return data


def insert_sort(data):
    for i in range(1, len(data)):
        for j in range(i, 0, -1):
            if data[j] < data[j - 1]:
                data[j], data[j - 1] = data[j - 1], data[j]
                log(data, speed)
            else:
                break
    return data


def select_sort(data):
    _len = len(data)
    for i in range(_len):
        _min = i
        for j in range(i + 1, _len):
            if data[_min] > data[j]:
                _min = j
        if _min != i:
            data[_min], data[i] = data[i], data[_min]
            log(data, speed)
    return data


def _quick_sort(data, first, last):
    if first < last:
        log(data, speed)
        pos = partition(data, first, last)
        _quick_sort(data, first, pos - 1)
        _quick_sort(data, pos + 1, last)
        log(data, speed)


def partition(data, first, last):
    wall = first
    for pos in range(first, last):
        if data[pos] < data[last]:  # last is the pivot
            data[pos], data[wall] = data[wall], data[pos]
            wall += 1
    data[wall], data[last] = data[last], data[wall]

    return wall


def quick_sort(data):
    _quick_sort(data, 0, len(data)-1)


def main():
    data = list('▅▁▃▇▄▆█▂')
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
    parser.add_argument('-s', '--speed', dest='speed',choices=['slow' , 'fast'], default=' slow' ,)
    args = parser.parse_args()
    global speed
    speed = 0.3
    if args.speed == 'fast':
        speed = 0.5
    print(_map[args.method].__name__)
    _map[args.method](data)


if __name__ == '__main__':
    main()
