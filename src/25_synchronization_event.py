import asyncio
import random

lera_list = []


async def func(event: asyncio.Event) -> None:
    count = 0
    while True:
        res = await asyncio.sleep(2, f"LERKA {random.randint(1, 5)}")
        lera_list.append(res)
        print(res)
        count += 1
        if count >= 5:
            event.set()
            break



async def main() -> None:
    lerka_ready_event = asyncio.Event()

    asyncio.Task(func(lerka_ready_event))

    await lerka_ready_event.wait()




if __name__ == '__main__':
    asyncio.run(main())
