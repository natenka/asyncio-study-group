import asyncio
import logging
import random

async def coro1(a, b):
    print('coro1', a)
    await asyncio.sleep(random.uniform(0,5))
    print('coro1 ends', a)
    return a+b

def func2(summ):
    print('func2', summ)
    return summ


if __name__ == '__main__':
    log = logging.getLogger('asyncio')
    log.setLevel(logging.DEBUG)

    result1 = [coro1(i,i) for i in range(1,10)]

    loop = asyncio.get_event_loop()
    loop.set_debug(True)
    group = result1

    all_data = []
    while group:
        done, undone = loop.run_until_complete(
            asyncio.wait(group,
                         return_when=asyncio.FIRST_COMPLETED))
        #print('###Done', done)
        #print('###Undone', undone)
        all_data.extend([func2(t.result()) for t in done ])
        print(all_data)
        group = undone

