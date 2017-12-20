#!/usr/bin/env python
# @Author  : pengyun

from types import coroutine
from collections import deque
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

# 通过下面这俩函数来调度。
@coroutine
def read_wait(sock):
    yield 'read_wait', sock
@coroutine
def write_wait(sock):
    yield 'write_wait', sock

class Loop:
    def __init__(self):
        self.ready = deque
        self.selector = DefaultSelector

    # 将之前阻塞的函数异步化，在读取或者写入这个过程异步。
    # 相当于是在应用层这一块实现了异步。

    async def sock_recv(self, sock, data):
        await read_wait(sock)
        return sock.recv(data)

    async def sock_accept(self, sock):
        await read_wait(sock)
        return sock.accept()

    async def sock_sendall(self, sock, data):
        while data:
            try:
                asent = sock.send(data)
                data = data[asent:]
            except BlockingIOError:
                await write_wait(sock)

    def create_task(self, coro):
        self.ready.append(coro)

    def run_forever(self):
        """维持一个事件循环，通过外面写的协程函数来调度。"""
        while True:
            while not self.ready:
                event = self.selector.select() # 通过提供的io复用接口拿到一条链接。
                for k, _ in event:
                    self.ready.append(k.data)
                    self.selector.unregister(k.fileobj)
            while self.ready:
                self.current_task = self.ready.popleft()
                try: # 调用外面的协程函数
                    op, *args = self.current_task.send(None)
                    getattr(self, op)(*args) # 调用相应的函数
                except StopIteration:
                    pass

    def read_wait(self, sock):
        self.selector.register(sock, EVENT_READ, self.current_task)

    def write_wait(self, sock):
        self.selector.register(sock, EVENT_WRITE, self.current_task)



