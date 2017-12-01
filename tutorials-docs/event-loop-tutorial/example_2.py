import asyncio
import time

async def my_work():
    print('Starts')
    time.sleep(5)
    print("I'm done")


loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(my_work())
finally:
    loop.close()

