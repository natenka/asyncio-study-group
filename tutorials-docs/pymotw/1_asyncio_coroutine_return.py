import asyncio

async def coroutine():
    print("Leave me alone! I'm working")
    return "Now i'm done"

event_loop = asyncio.get_event_loop()

try:
    return_value = event_loop.run_until_complete(coroutine())
    print('That sneaky coroutine returned this:', return_value)
finally:
    event_loop.close()
