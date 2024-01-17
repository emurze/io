import asyncio
import functools
import time
from collections.abc import Callable
from typing import Any

import aiohttp


def limit_rate(limit: int = 5) -> Callable:
    def wrapper(coro: Callable) -> Callable:
        semaphore = asyncio.Semaphore(limit)

        @functools.wraps(coro)
        async def inner_coro(*args, **kwargs) -> Any:
            async with semaphore:
                return await coro(*args, **kwargs)

            # await semaphore.acquire()
            # res = await coro(*args, **kwargs)
            # semaphore.release()
            # return res

        return inner_coro

    return wrapper



@limit_rate()
async def make_request(url: str) -> None:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.json()
            print(data)
            await asyncio.sleep(5)
            print('--------')


async def main() -> None:
    start = time.monotonic()

    tasks = [
        asyncio.Task(make_request('http://0.0.0.0:8000/hello'))
        for _ in range(20)
    ]
    await asyncio.gather(*tasks)

    print(time.monotonic() - start)


if __name__ == '__main__':
    asyncio.run(main())
