import asyncio

#Tasks are one of the primary ways to interact with the event loop.
#Tasks wrap coroutines and track when they are complete.
#Tasks are subclasses of Future, so other coroutines can wait
#for them and each has a result that can be retrieved after the task completes.

async def task_func():
    print('in task_func')
    return 'the result'


async def main(loop):
    print('creating task')
    task = loop.create_task(task_func())
    print('waiting for {!r}'.format(task))
    return_value = await task
    print('task completed {!r}'.format(task))
    print('return value: {!r}'.format(return_value))


event_loop = asyncio.get_event_loop()
try:
    event_loop.run_until_complete(main(event_loop))
finally:
    event_loop.close()

