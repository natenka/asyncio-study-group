import asyncio
import logging
import random


async def coro1(a, b):
    print('coro1', a)
    await asyncio.sleep(random.uniform(0,5))
    print('coro1 ends', a)
    return a+b


async def coro2(summ):
    print('coro2', summ)
    return summ


if __name__ == '__main__':
    log = logging.getLogger('asyncio')
    log.setLevel(logging.DEBUG)

    result1 = [coro1(i,i) for i in range(1,10)]

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    group = result1

    while group:
        done, undone = loop.run_until_complete(
            asyncio.wait(group,
                         return_when=asyncio.FIRST_COMPLETED))
        #print('###Done', done)
        #print('###Undone', undone)
        tasks = [loop.create_task(coro2(t.result())) for t in done ]
        loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            print(task.result())
        group = undone

