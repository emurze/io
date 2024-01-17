import asyncio


async def coro_func() -> None:
    print('start coro func')
    await asyncio.sleep(1)
    print('end coro func')


async def main() -> None:
    print('-- start main')

    asyncio.Task(coro_func())

    await asyncio.sleep(.5)

    print('-- end main')



if __name__ == '__main__':
    asyncio.run(main())  # run feature
