import asyncio
import time

import aiohttp

lock = asyncio.Lock()


async def make_request(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with lock:
            async with session.get(url) as response:
                await asyncio.sleep(.2)
                return await response.json()



async def no_lock_make_request(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


async def func(url: str) -> None:
    response = await make_request(url)
    print(response)


async def no_lock_func(url: str) -> None:
    response = await no_lock_make_request(url)
    print(response)


async def main() -> None:
    start = time.monotonic()

    tasks = [
        asyncio.Task(func('http://0.0.0.0:8000/hello'))
        for _ in range(20)
    ]
    no_lock_tasks = [
        asyncio.Task(no_lock_func('http://0.0.0.0:8000/hello_world'))
        for _ in range(5)
    ]
    await asyncio.gather(*tasks, *no_lock_tasks)

    print(time.monotonic() - start)


if __name__ == '__main__':
    asyncio.run(main())
