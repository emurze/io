import asyncio
from asyncio import Future


async def wait_for(task: Future, timeout: int) -> Future:
    secs = 0
    while not task.done():
        if secs == timeout:
            task.cancel()
        await asyncio.sleep(1)
        secs += 1
    return await task


async def greet(timeout: int):
    await asyncio.sleep(timeout)
    return 'Hello World!'


async def main() -> None:
    task = asyncio.Task(greet(3))

    try:
        res = await wait_for(task, 2)
        print(res)
    except asyncio.CancelledError:
        print('Task cancelled')


if __name__ == '__main__':
    asyncio.run(main())
