import asyncio
import datetime
from concurrent.futures import CancelledError

async def display_date(task_id):
    msg = '##### Task ID: {task_id} Call ID: {call} {date}'
    try:
        print(msg.format(task_id=task_id, call=1, date=datetime.datetime.now()))
        await asyncio.sleep(2)
        print(msg.format(task_id=task_id, call=2, date=datetime.datetime.now()))
        await asyncio.sleep(2)
        print(msg.format(task_id=task_id, call=3, date=datetime.datetime.now()))
    except CancelledError as exc:
        print(exc)
        print("It's task {task_id} I'm cancelling myself...".format(task_id=task_id))


async def cancel_another_task(task_id, task_to_cancel):
    msg = '##### Task ID: {task_id} Call ID: {call}'
    print(msg.format(task_id=task_id, call=1))
    await asyncio.sleep(1)
    print(msg.format(task_id=task_id, call=2))
    await asyncio.sleep(1)
    print('This is task {task_id}. I will cancel someone at call {call}'.format(
                                               task_id=task_id, call=3))
    task_to_cancel.cancel()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    task1 = loop.create_task(display_date(1))
    task2 = loop.create_task(cancel_another_task(2, task1))
    task3 = loop.create_task(display_date(3))

    loop.run_until_complete(asyncio.gather(task1, task2, task3))
    loop.close()

