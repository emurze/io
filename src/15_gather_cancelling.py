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
    except asyncio.CancelledError:
        print('ROLLBACK TRANSACTION')
        raise asyncio.CancelledError


async def main() -> None:
    task1 = asyncio.Task(value_error(), name='value error')
    task2 = asyncio.Task(type_error(), name='type error')
    task3 = asyncio.Task(hello(1), name='long coro')
    tasks = [task1, task2, task3]

    try:
        results = await asyncio.gather(*tasks)
    except ValueError as e:
        print(f'{e=}')
    except TypeError as e:
        print(f'{e=}')
    else:
        print(results)

    for task in tasks:
        if task.done() is False:
            print(f'Pending: {task.get_name()}')
            task.cancel()

    await asyncio.sleep(2)
    print(task1._state)
    print(task2._state)
    print(task3._state)


if __name__ == '__main__':
    asyncio.run(main())
