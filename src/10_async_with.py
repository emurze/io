import asyncio

import aiohttp


class AsyncSession:
    def __init__(self, url: str) -> None:
        self._url = url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        response = await self.session.get(self._url)
        return response

    async def __aexit__(self, *args) -> None:
        await self.session.close()


async def main() -> None:
    """
    session = AsyncSession('https://example.com')
    response = await session.__aenter__()
    print(response)
    await session.__aexit__()
    """

    async with AsyncSession('https://example.com') as response:
        print(response)


if __name__ == "__main__":
    asyncio.run(main())
