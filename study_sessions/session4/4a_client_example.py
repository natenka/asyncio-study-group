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
            raise TypeError("Erooooooorrrrrr")
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
for task in tasks:
    try:
        task.result()
    except asyncio.TimeoutError as e:
        print('Error', e)
    except TypeError as e:
        print(task.exception())
    else:
        print(task.result())
print('The End')
