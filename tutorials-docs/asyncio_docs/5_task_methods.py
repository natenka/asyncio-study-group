import asyncio
import datetime

async def display_date():
    print('#'*10, datetime.datetime.now())
    await asyncio.sleep(2)
    print('#'*10, datetime.datetime.now())
    await asyncio.sleep(2)
    print('#'*10, datetime.datetime.now())

async def show_task_stack(task_to_explore):
    print(task_to_explore.print_stack())
    await asyncio.sleep(1)
    print(task_to_explore.print_stack())
    await asyncio.sleep(1)
    print(task_to_explore.print_stack())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(display_date())
    task2 = loop.create_task(show_task_stack(task1))

    loop.run_until_complete(asyncio.gather(task1, task2))
    loop.close()

