import asyncio
import time
from datetime import datetime


async def async_print(my_id):
    print("     Started  {} at {}".format(my_id, datetime.now()))
    await asyncio.sleep(my_id)
    print("     Finished {} at {}".format(my_id, datetime.now()))


async def async_square(number):
    await async_print(number)
    result = number ** 2
    print("Square of {} is {} at {}".format(number, result, datetime.now()))
    return result


if __name__ == '__main__':
    start_time = time.time()
    print("Started at : {}". format(datetime.now()))

    loop = asyncio.get_event_loop()

    for i in range(5):
        loop.create_task(async_square(i))
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()
        print('\nIt took {} seconds to run'.format(time.time() - start_time))

