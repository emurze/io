import asyncio


async def print_seconds():
    for i in range(100):
        print(i)
        await asyncio.sleep(.1)


async def main() -> None:
    task1 = asyncio.Task(print_seconds())  # type: ignore
    task2 = asyncio.Task(print_seconds())  # type: ignore

    await task1
    # yield from asyncio.gather(task1, task2)  # select


if __name__ == '__main__':
    asyncio.run(main())
