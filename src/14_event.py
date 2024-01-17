import asyncio


async def func(event: asyncio.Event) -> None:
    for i in range(100):
        print(i * i)
        if i == 50:
            event.set()
            await asyncio.sleep(0)


async def trigger(event: asyncio.Event) -> None:
    await event.wait()
    print('done')


async def main() -> None:
    event = asyncio.Event()
    await asyncio.gather(trigger(event), func(event))


if __name__ == '__main__':
    asyncio.run(main())
