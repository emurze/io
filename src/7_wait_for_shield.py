import asyncio


async def greet(timeout):
    await asyncio.sleep(timeout)
    print(timeout)


async def main():
    task = asyncio.Task(greet(4))

    try:
        await asyncio.wait_for(
            asyncio.shield(task),  # without cancelled behavior
            timeout=3,
        )
    except asyncio.TimeoutError:
        print("Task greet(60) don't executed after 3 seconds")
        await task



if __name__ == '__main__':
    asyncio.run(main())
