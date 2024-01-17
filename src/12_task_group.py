import asyncio
from typing import NoReturn


async def hello_error() -> NoReturn:
    raise ValueError("hello world")


async def hell_error() -> NoReturn:
    raise TypeError("hello world")


async def hello(m) -> str:
    await asyncio.sleep(1)
    return f'{m=}'


async def main() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(hello_error())
            task2 = tg.create_task(hell_error())
            task3 = tg.create_task(hell_error())

        print(task1.result())
        print(task2.result())
        print(task3.result())

    except* ValueError as e:
        print(f"{e=}")
    except* TypeError as e:
        print(f"{e=}")



asyncio.run(main())
