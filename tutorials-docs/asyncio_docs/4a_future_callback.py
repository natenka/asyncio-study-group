import asyncio

async def coro1(num):
    await asyncio.sleep(1)
    return num**2

def got_result(future):
    print(future.result())
    loop.stop()

loop = asyncio.get_event_loop()

task = asyncio.ensure_future(coro1(5))
task.add_done_callback(got_result)

try:
    loop.run_forever()
finally:
    loop.close()
