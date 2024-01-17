import asyncio
from collections.abc import AsyncGenerator

from faker import Faker

faker = Faker('en_US')


async def timer(count: int = 0) -> None:
    while True:
        count += 1
        print(count)
        await asyncio.sleep(.001)


async def get_name(amount: int) -> AsyncGenerator:
    for _ in range(amount):
        await asyncio.sleep(.001)
        name, surname, *_ = faker.name_male().split()
        yield name, surname


async def main() -> None:
    asyncio.Task(timer(5))
    async for name, surname in get_name(50):
        print({name: surname})

    print({name: surname async for name, surname in get_name(50)})


if __name__ == '__main__':
    asyncio.run(main())
