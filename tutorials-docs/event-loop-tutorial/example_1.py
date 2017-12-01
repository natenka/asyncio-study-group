import asyncio

async def my_coroutine():
    print("I'm working here!")

loop = asyncio.get_event_loop()
try:
    loop.run_until_complete(my_coroutine())
finally:
    loop.close()


