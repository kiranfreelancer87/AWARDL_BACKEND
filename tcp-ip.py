import aiohttp
import asyncio
import time
import socket

start_time = time.time()


async def main():
    connector = aiohttp.TCPConnector(local_addr=('2a05:4e0::1', 0), family=socket.AF_INET6)
    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for x in range(5):
            task = asyncio.ensure_future(fetch(session, x))
            tasks.append(task)

        response_ = await asyncio.gather(*tasks)
        print(response_)


async def fetch(session, x):
    url = f'http://ipv6.google.com/'

    async with session.get(url) as response:
        result_data = await response.text()
        return x


asyncio.run(main())

print("--- %s seconds ---" % (time.time() - start_time))
