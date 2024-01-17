import asyncio


async def hello() -> None:
    print('Hello World!')


async def one_hundred_tasks() -> None:
    for _ in range(100):
        # await asyncio.sleep(0)  Cringe printed first or last
        await hello()


async def cringe() -> None:
    print('Cringe')


async def make_request(session, url: str):
    response = await session.get(url)
    return response.real_url


async def greet(timeout: float) -> int:
    await asyncio.sleep(timeout)
    print(f'Hello, {timeout}')
    return int(timeout) * 1111111


async def main() -> None:
    # coroutines = [
    #     greet(.5 * index)
    #     for index in range(10)
    # ]
    # 1. Run all coroutines
    # 2. Await for first done in queue
    # results = [await coro for coro in asyncio.as_completed(coroutines)]

    # 1. Run all task
    # 2. Await for total result
    # res_list = await asyncio.gather(
    #     *coroutines,
    #     server_error("Vlad isn't danger master. Please send another one"),
    #     return_exceptions=True,
    # )

    # 1. Run async group from several gather futures
    # red_burgers = asyncio.gather(greet(1), greet(2))
    # blue_burgers = asyncio.gather(greet(.5), greet(1))
    # burger_group = asyncio.gather(red_burgers, blue_burgers)

    task1 = asyncio.Task(one_hundred_tasks())
    task2 = asyncio.Task(cringe())

    # Await has async behavior only with I/O operations inside
    await asyncio.gather(task1, task2)




if __name__ == "__main__":
    asyncio.run(main())
