import asyncio
import random
from concurrent.futures import ThreadPoolExecutor


async def worker(condition: asyncio.Condition) -> None:
    while True:
        async with condition:
            await condition.wait()
            print(f'Hello world {random.randint(1, 5)}')


async def ainput(prompt: str = "") -> str:
    """
    Create async code from sync
    """

    loop = asyncio.get_event_loop()
    with ThreadPoolExecutor(1, "AsyncInput") as executor:
        return await loop.run_in_executor(executor, input, prompt)


async def notifier(condition: asyncio.Condition) -> None:
    while True:
        res = await ainput("What's your name? ")
        print(res)
        await asyncio.sleep(3)

        async with condition:
            # condition.notify_all()
            condition.notify(3)


async def main():
    condition = asyncio.Condition()
    tasks = [
        asyncio.Task(worker(condition)) for _ in range(10)
    ]
    await asyncio.gather(*tasks, notifier(condition))




if __name__ == '__main__':
    asyncio.run(main())
