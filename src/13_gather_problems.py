import asyncio


async def hello() -> None:
    print('Hello World!')
    raise ValueError('Lera')


async def one_hundred_tasks() -> None:
    for _ in range(100):
        # await asyncio.sleep(0)  Cringe printed first or last
        await hello()


async def cringe() -> None:
    print('Cringe')
    raise TypeError('Vlad')


async def greet(timeout: float) -> int:
    await asyncio.sleep(timeout)
    print(f'Hello, {timeout}')
    return int(timeout) * 1111111


async def main() -> None:
    # 1 error and stop instead of 2 errors
    try:
        res = await asyncio.gather(greet(0), hello(), cringe())
    except ValueError as e:
        print(f'{e=}')
    except TypeError as e:
        print(f'{e=}')
    else:
        print(res)


asyncio.run(main())
