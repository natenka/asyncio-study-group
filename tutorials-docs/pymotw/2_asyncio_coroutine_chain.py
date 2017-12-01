import asyncio

async def outer():
    print("Now you are inside outer")
    print("Waiting for result from phase 1")
    result1 = await phase1()
    print("Waiting for result from phase 2")
    result2 = await phase2(result1)


async def phase1():
    print("In phase1")
    return "result1"

async def phase2(arg):
    print("In phase2")
    return "Result from {}".format(arg)

event_loop = asyncio.get_event_loop()

try:
    return_value = event_loop.run_until_complete(outer())
    print('return value: {!r}'.format(return_value))
finally:
    event_loop.close()

