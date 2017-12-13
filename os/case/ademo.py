#!/usr/bin/env python
# @Author  : pengyun

# 用来理解为什么代码要完全异步化。


import asyncio
import time

async def greeting_with_sync(name):
    if name == 'Thomas':
        time.sleep(1) # 在这里将整个进程block掉
    return 'Hello ' + name

async def greeting(name):
    if name == 'Thomas':
        await asyncio.sleep(0.1)
    return 'Hello ' + name


async def runmain(func):
    names = ['Dave', 'Paula', 'Thomas', 'Lewis']
    for name in names:
        print(await func(name))

async def run(loop, func):
    workers = [asyncio.Task(runmain(func), loop=loop)
               for _ in range(7)]
    for w in workers:
        await asyncio.sleep(0.2)
        await w
        w.done()


def main():
    start = time.time()
    print("Async mode")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop, greeting))
    print(time.time() - start)

    start = time.time()
    print("Async with sync")
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run(loop, greeting_with_sync))
    print(time.time() - start)

if __name__ == '__main__':
    main()