import asyncio
import datetime


async def anything(i):
    print(i, 'start time', datetime.datetime.now())
    await asyncio.sleep(i)
    print(i, 'stop  time', datetime.datetime.now())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.call_later(2, loop.stop)

    for i in range(1, 4):
        #call_soon не подходит для вызова сопрограммы
        #loop.call_soon(anything, i)
        #для вызова сопрограммы ее надо обернуть в задачу
        loop.create_task(anything(i))
    try:
        loop.run_forever()
    finally:
        loop.close()


#В таком варианте задачи не успевают выполниться,
#так как через две секунды loop закрывается
'''
$ python 3_coroutine_function.py
1 start time 2017-12-01 13:34:53.602866
2 start time 2017-12-01 13:34:53.603359
3 start time 2017-12-01 13:34:53.603653
1 stop  time 2017-12-01 13:34:54.605682
Task was destroyed but it is pending!
task: <Task pending coro=<anything() running at 3_coroutine_function.py:7>
                    wait_for=<Future finished result=None>>
Task was destroyed but it is pending!
task: <Task pending coro=<anything() done, defined at 3_coroutine_function.py:5>
                    wait_for=<Future pending
                          cb=[<TaskWakeupMethWrapper object at 0xb6caa464>()]>>
'''
