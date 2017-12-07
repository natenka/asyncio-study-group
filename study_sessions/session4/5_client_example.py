from pprint import pprint
import asyncio
import async_timeout
import aiohttp
import concurrent.futures


async def fetch(url):
    result_dict = {}
    async with aiohttp.ClientSession(read_timeout=3) as session:
        try:
            async with session.get(url) as response:
                result_dict['url'] = url
                raise TypeError
                #result_dict['status'] = response.status
                #result_dict['method'] = response.method
                #result_dict['content_type'] = response.content_type
                #result_dict['text'] = await response.text()
                #if result_dict['content_type'] == 'application/json':
                #    result_dict['json'] = await response.json()
        except asyncio.TimeoutError as e:
            print('Error', e)
    return result_dict



urls = ['https://api.github.com/users/natenka',
        'https://httpbin.org/delay/10',
        'https://api.github.com/users/pyneng']
loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(fetch(url)) for url in urls]
results = loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
print(results)
print('The End')
