#!/usr/bin/env python
# @Author  : pengyun

from socket import *
import aplay

loop = aplay.Loop()

async def echo_serer(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    sock.setblocking(False)
    while True:
        client, addr = await loop.sock_accept(sock)
        loop.create_task(echo_handler(client))

async def echo_handler(client):
    """将请求的数据回送回去"""
    with client:
        while True:
            # block ！ 读写的时候会在这里block，利用一个循环同时管理多个
            # 连接。如果一个链接需要较长时间来获取数据，就先去处理另一个链接
            # 而不是被一个链接阻塞。
            data = await client.sock_recv(client, 8192)
            if not data:
                break
            await loop.sock_sendall(client, data)
    print('Connection close')
