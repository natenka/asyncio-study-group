import asyncio

async def work():
    while True:
        await asyncio.sleep(1)
        print('One more task is done')


loop = asyncio.get_event_loop()

try:
    asyncio.ensure_future(work())
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print("Closing loop")
    loop.close()

