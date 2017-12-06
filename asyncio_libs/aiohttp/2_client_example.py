from pprint import pprint
import asyncio
import async_timeout
import aiohttp


async def fetch(session, url):
    result_dict = {}
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            result_dict['url'] = url
            result_dict['status'] = response.status
            result_dict['method'] = response.method
            result_dict['content_type'] = response.content_type
            result_dict['text'] = await response.text()
            if result_dict['content_type'] == 'application/json':
                result_dict['json'] = await response.json()
    return result_dict


async def main(urls):
    for url in urls:
        async with aiohttp.ClientSession() as session:
            data = await fetch(session, 'https://api.github.com/users/natenka')
            pprint(data)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(['https://api.github.com/users/natenka']))
