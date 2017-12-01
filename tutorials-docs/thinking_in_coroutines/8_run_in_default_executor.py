import time
import datetime
import asyncio


def blocking_call(seconds):
    print(seconds, datetime.datetime.now())
    time.sleep(seconds)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(5, loop.stop)
    for i in range(1,4):
        #по умолчанию используется concurrent.futures.ThreadPoolExecutor
        # для этого надо передать executor = None
        #количество потоков по умолчанию:
        #number of processors on the machine, multiplied by 5
        loop.run_in_executor(None, blocking_call, i)
    try:
        loop.run_forever()
    finally:
        loop.close()

