from pprint import pprint
import asyncio
import async_timeout
import aiohttp
import concurrent.futures


async def fetch(url):
    result_dict = {}
    async with aiohttp.ClientSession(read_timeout=3) as session:
        async with session.get(url) as response:
            result_dict['url'] = url
            result_dict['status'] = response.status
            result_dict['method'] = response.method
            result_dict['content_type'] = response.content_type
            result_dict['text'] = await response.text()
            if result_dict['content_type'] == 'application/json':
                result_dict['json'] = await response.json()
    return result_dict['url']



urls = ['https://api.github.com/users/natenka',
        'https://httpbin.org/delay/10',
        'https://api.github.com/users/pyneng']
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(fetch(url)) for url in urls]
results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
print(results)
for result in results:
    if isinstance(result, BaseException):
        print('Error')
    else:
        print(result)
print('The End')
#прочитала, что лучше использовать ensure_future вместо create_task
'''
ensure_future is method to create Task from coroutine. It creates task different ways based on argument (including using of create_task for coroutines and future-like objects).

create_task is abstract method of AbstractEventLoop. Different event loops can implement this function different ways.

https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine


Another important difference is that in addition to accepting coroutines, ensure_future also accepts any awaitable object; create_task on the other hand just accepts coroutines.

https://stackoverflow.com/questions/33980086/whats-the-difference-between-loop-create-task-asyncio-async-ensure-future-and
'''
