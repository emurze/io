import asyncio
import random


class Color:
    norm = '\033[0m'
    blue = '\033[94m'
    green = '\033[92m'


c = Color()
QUEUE_MAX_SIZE = 3


async def consumer(queue: asyncio.Queue, name: str) -> None:
    while True:
        timeout = await queue.get()
        await asyncio.sleep(timeout)
        queue.task_done()
        print(f'{c.green}Consumer {name} ate {timeout} from {queue}{c.norm}')


async def producer(queue: asyncio.Queue, name: str) -> None:
    timeout = random.randint(1, 3)
    await queue.put(timeout)
    print(f'{c.blue}Producer {name} put {timeout} to {queue}{c.norm}')


async def main() -> None:
    """
    1. Queue(maxsize)
    2. .put()
       .get()
       .join()
       .empty()
       .task_done()
    """

    queue = asyncio.Queue(maxsize=QUEUE_MAX_SIZE)

    consumers = [
        asyncio.Task(consumer(queue, f'consumer_{index}'))
        for index in range(3)
    ]

    producers = [
        asyncio.Task(producer(queue, f'producer_{index}'))
        for index in range(12)
    ]

    await asyncio.gather(*producers)
    await queue.join()

    for cons in consumers:
        cons.cancel()



if __name__ == '__main__':
    asyncio.run(main())
