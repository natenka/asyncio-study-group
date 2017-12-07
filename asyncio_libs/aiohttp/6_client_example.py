from pprint import pprint
import asyncio
import async_timeout
import aiohttp


async def fetch(url):
    result_dict = {}
    async with aiohttp.ClientSession(read_timeout=3) as session:
        async with session.get(url) as response:
            result_dict['url'] = url
            #result_dict['status'] = response.status
            #result_dict['method'] = response.method
            #result_dict['content_type'] = response.content_type
            #result_dict['text'] = await response.text()
            #if result_dict['content_type'] == 'application/json':
            #    result_dict['json'] = await response.json()
        print(result_dict)
    return result_dict



urls = ['https://api.github.com/users/natenka',
        'https://httpbin.org/delay/10',
        'https://api.github.com/users/pyneng']
loop = asyncio.get_event_loop()
task = loop.create_task(fetch(urls[0]))
try:
    loop.run_forever()
except KeyboardInterrupt:
    print('The End')
finally:
    loop.close()
