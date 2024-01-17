import asyncio


async def value_error():
    raise ValueError("hello world")


async def type_error():
    raise TypeError("hello world")


async def hello(m) -> str:
    try:
        print('Start Long coro')
        await asyncio.sleep(1)
        print('END Long coro')
        return f'{m=}'
    except asyncio.CancelledError:  # action on Cancel
        print('ROLLBACK TRANSACTION')
        raise asyncio.CancelledError


async def main() -> None:
    try:
        async with asyncio.TaskGroup() as tg:
            task1 = tg.create_task(value_error(), name='value error')
            task2 = tg.create_task(type_error(), name='type error')
            task3 = tg.create_task(hello(1), name='long coro')

    except* TypeError as e:
        print(f'{e=}')

    except* ValueError as e:
        print(f'{e=}')




if __name__ == '__main__':
    asyncio.run(main())
