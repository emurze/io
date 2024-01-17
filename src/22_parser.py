import asyncio
from asyncio import Queue, Task, get_running_loop
from collections.abc import Callable
from concurrent.futures import ProcessPoolExecutor
from typing import cast

import aiofiles
import aiohttp
from aiohttp import ClientSession, ClientResponse
from bs4 import BeautifulSoup

URL = 'https://c.xkcd.com/random/comic'
IMAGE_DIR = 'images'
WAIT_TIMEOUT = 10


class BaseDownloader:
    def __init__(
        self,
        session: ClientSession,
        url: str,
        timeout: int = 5,
    ) -> None:
        self.session = session
        self.url = url
        self.timeout = timeout

    @staticmethod
    def cancel_tasks(tasks: list[Task]) -> None:
        for task in tasks:
            task.cancel()

    @staticmethod
    def create_tasks(workers: int, coro: Callable, *args) -> list[Task]:
        return [Task(coro(*args)) for _ in range(workers)]

    async def gather(self, tasks: list[Task], timeout: int = 0):
        return await asyncio.gather(
            *[asyncio.wait_for(i, timeout or self.timeout) for i in tasks],
            return_exceptions=True,
        )

    async def join(self, queue: Queue, timeout: int = 0) -> None:
        try:
            await asyncio.wait_for(queue.join(), timeout or self.timeout)
        except TimeoutError:
            pass

    async def make_request(self, url: str) -> ClientResponse:
        response = await self.session.get(url)
        if response.ok:
            return response
        else:
            print('Request error')


class Downloader(BaseDownloader):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.done_tasks = 0

    @staticmethod
    def parse_image_url(html) -> str | None:
        """
        TASK
        """

        bs = BeautifulSoup(html, 'lxml')

        if img := bs.select_one('#comic>img'):
            image_url = f"https:{img.get('src')}"
            return image_url

    async def get_image_page(self, pages_queue: Queue) -> None:
        page = await self.make_request(self.url)
        print(f"Page {page.url} is added to queue")
        await pages_queue.put(page.url)

    async def get_image_url(
        self,
        pages_queue: Queue,
        image_queue: Queue,
    ) -> None:
        while True:
            url = await pages_queue.get()
            response = await self.make_request(url)
            html = await response.text()

            loop = get_running_loop()
            with ProcessPoolExecutor() as pool:
                image_url = await loop.run_in_executor(
                    pool, self.parse_image_url, html
                )

            if image_url is not None:
                await image_queue.put(image_url)
                print(f"Image Page {image_url} is added to queue")

            pages_queue.task_done()

    async def download_image(self, image_queue: Queue) -> None:
        while True:
            image_url = await image_queue.get()
            response = await self.make_request(image_url)
            filename = image_url.rsplit('/', 1)[-1]

            async with aiofiles.open(f'{IMAGE_DIR}/{filename}', 'wb') as f:
                async for chunk in response.content.iter_chunked(1024):
                    chunk: bytes = cast(bytes, chunk)  # pycharm linter bug
                    await f.write(chunk)

            print(f"Image {filename} downloaded")
            image_queue.task_done()
            self.done_tasks += 1

    async def run(self) -> None:
        pages_queue = Queue()
        image_queue = Queue()

        page_getters = self.create_tasks(
            10_000, self.get_image_page, pages_queue
        )

        await self.gather(page_getters)

        image_getters = self.create_tasks(
            500,
            self.get_image_url,
            pages_queue,
            image_queue
        )

        await self.join(pages_queue)
        self.cancel_tasks(image_getters)

        downloaders = self.create_tasks(500, self.download_image, image_queue)

        await self.join(image_queue)
        self.cancel_tasks(downloaders)

        print(self.done_tasks)


async def main() -> None:
    async with aiohttp.ClientSession() as session:
        downloader = Downloader(session, URL, WAIT_TIMEOUT)
        await downloader.run()


if __name__ == '__main__':
    asyncio.run(main())
