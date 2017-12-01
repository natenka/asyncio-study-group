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
    loop = asyncio.get_event_loop()
    tasks = [loop.create_task(anything(i))
             for i in range(1, 4)]
    try:
        loop.run_until_complete(asyncio.wait(tasks))
        for task in tasks:
            print(*task.result())
    finally:
        loop.close()


