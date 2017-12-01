import asyncio
import time
from datetime import datetime

def blocking_print(msg):
    print("Start  {} at {}".format(msg, datetime.now()))
    time.sleep(1)
    print("Finish {} at {}".format(msg, datetime.now()))
    return

if __name__ == '__main__':
    start_time = time.time()
    print("Started at : {}". format(datetime.now()))

    loop = asyncio.get_event_loop()
    loop.call_later(5, blocking_print, 'called using call_later')

    for i in range(5):
        loop.call_soon(blocking_print, 'called using call_soon')
    loop.call_later(2, loop.stop)
    try:
        loop.run_forever()
    finally:
        loop.close()

    print('It took {} seconds to run'.format(time.time() - start_time))


