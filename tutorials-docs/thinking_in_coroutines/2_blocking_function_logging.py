import asyncio
import time
import datetime


def anything(i):
    print(i, 'start time', datetime.datetime.now())
    time.sleep(2)
    print(i, 'stop  time', datetime.datetime.now())

if __name__ == '__main__':
    import logging
    log = logging.getLogger('asyncio')
    log.setLevel(logging.DEBUG)

    loop = asyncio.get_event_loop()
    loop.set_debug(True)

    loop.call_later(2, loop.stop)

    for i in range(1, 4):
        loop.call_soon(anything, i)
    try:
        loop.run_forever()
    finally:
        loop.close()
