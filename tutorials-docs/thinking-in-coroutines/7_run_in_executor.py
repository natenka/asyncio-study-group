import time
import datetime
import asyncio
from concurrent.futures import ThreadPoolExecutor


def blocking_call(seconds):
    print(seconds, datetime.datetime.now())
    time.sleep(seconds)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(5, loop.stop)
    with ThreadPoolExecutor(max_workers=5) as executor:
        for i in range(1,4):
            loop.run_in_executor(executor, blocking_call, i)
        try:
            loop.run_forever()
        finally:
            loop.close()

