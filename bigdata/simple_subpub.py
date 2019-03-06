#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Created on    : 2018/12/27 11:36 AM
# @Author  : zpy
# @Software: PyCharm

from socket import *
from collections import defaultdict
import argparse

_map = defaultdict(list)

def sub_pubserver(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print('Connect: {}'.format(addr))
        sub_pub_handle(client)

def sub_pub_handle(client):
    """
    # sub xxxx
    # pub xxxx  xxxx
    :param client:
    :return:
    """
    data = client.recv(1024)

    d = data.decode().split(' ')
    print(d)
    if len(d) > 2:
        ttype, channel, msg = d
    else:
        ttype, channel = d
    if ttype == 'sub':
        _map[channel].append(client)
    if ttype == 'pub':
        for suber in _map[channel]:
            suber.sendall(msg.encode())

def sp_client(ip_port):
    sk = socket(AF_INET, SOCK_STREAM, 0)
    sk.connect(ip_port)

    inp = input('>>>').strip()
    if inp.startswith('sub') or inp.startswith('pub'):
        if inp.startswith('sub'):
            print(sk.recv(1024))
        elif inp.startswith('sub'):
            while True:
                sk.send(inp.encode())
                inp = input('>>>').strip()

    sk.close()

def main():
    parser = argparse.ArgumentParser(description="Input servername")
    parser.add_argument("-s", '-server', dest="server", default=False)
    parser.add_argument("-sp", '-subribe', dest="sp", default=False)
    parser.add_argument("-pub", '-publish', dest="pub", default=False)
    args = parser.parse_args()

    if args.sp:
        addr = args.sp
    else:
        addr = args.server
    try:
        host, port = addr.split(':')
        port = int(port)
    except:
        print("host:port")
        return

    if args.sp:
        sp_client((host, port))
    else:
        sub_pubserver((host, port))

if __name__ == '__main__':
    main()