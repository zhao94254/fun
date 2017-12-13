#!/usr/bin/env python
# @Author  : pengyun

from socket import *

def echo(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print('Connect: {}'.format(addr))
        echo_handler(client)

def echo_handler(client):
    with client:
        while True:
            data = client.recv(4096)
            if not data:
                break
            client.sendall(data)
    print("Connect close")

if __name__ == '__main__':
    echo(address=('localhost', 20000))


