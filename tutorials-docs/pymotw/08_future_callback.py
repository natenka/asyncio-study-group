import asyncio
import functools


def callback(future, n):
    print('{}: future done: {}'.format(n, future.result()))

#The callback should expect one argument, the Future instance.
#To pass additional arguments to the callbacks,
# use functools.partial() to create a wrapper.

async def register_callbacks(all_done):
    print('registering callbacks on future')
    all_done.add_done_callback(functools.partial(callback, n=1))
    all_done.add_done_callback(functools.partial(callback, n=2))


async def main(all_done):
    await register_callbacks(all_done)
    print('setting result of future')
    all_done.set_result('the result')


event_loop = asyncio.get_event_loop()
try:
    all_done = asyncio.Future()
    event_loop.run_until_complete(main(all_done))
finally:
    event_loop.close()

