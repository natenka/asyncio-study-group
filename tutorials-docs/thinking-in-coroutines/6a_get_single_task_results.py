
import asyncio
import datetime


async def anything(idx):
    print(idx, 'start time', datetime.datetime.now())
    #В asyncio.sleep можно указывать аргумент result,
    #который будет возвращаться после выполнения
    result = await asyncio.sleep(idx, result='Done')
    #print('asyncio.sleep results:', result)
    print(idx, 'stop  time', datetime.datetime.now())
    return idx, datetime.datetime.now()


if __name__ == '__main__':
    ## version2
    loop = asyncio.get_event_loop()
    try:
        result = loop.run_until_complete(anything(3))
        print(*result)
    finally:
        loop.close()
