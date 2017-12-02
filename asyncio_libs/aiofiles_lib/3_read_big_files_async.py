import asyncio
import aiofiles


#It is a SyntaxError to use async with outside of an async def function.
async def read_file(filename):
    async with aiofiles.open(filename) as f:
        content = await f.readlines()
    return len(content)


async def main():
    files = ['test_files/rib.table.lg.ba.ptt.br-BGP1.csv',
             'test_files/rib.table.lg.ba.ptt.br-BGP2.csv',
             'test_files/rib.table.lg.ba.ptt.br-BGP3.csv',]

    coroutines = (read_file(f) for f in files)
    results = await asyncio.gather(*coroutines, return_exceptions=True)
    print(results)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())


'''
asyncio.gather(*coros_or_futures, loop=None, return_exceptions=False)
Return a future aggregating results from the given coroutine objects or futures.

All futures must share the same event loop.
If all the tasks are done successfully, the returned future’s result is the list of results (in the order of the original sequence, not necessarily the order of results arrival).
If return_exceptions is true, exceptions in the tasks are treated the same as successful results, and gathered in the result list; otherwise, the first raised exception will be immediately propagated to the returned future.

Cancellation: if the outer Future is cancelled, all children (that have not completed yet) are also cancelled. If any child is cancelled, this is treated as if it raised CancelledError – the outer Future is not cancelled in this case. (This is to prevent the cancellation of one child to cause other children to be cancelled.)
'''
