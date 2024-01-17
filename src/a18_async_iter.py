from contextlib import asynccontextmanager

from redis import asyncio as aioredis

from collections.abc import AsyncIterator

from fastapi import APIRouter, Depends

router = APIRouter()

#
# class RedisReader(AsyncIterator):
#     def __init__(self, redis: aioredis.Redis, keys: list) -> None:
#         self.redis = redis
#         self.keys = iter(keys)
#
#     def __aiter__(self) -> Self:
#         return self
#
#     async def __anext__(self) -> str:
#         try:
#             key = next(self.keys)
#         except StopIteration:
#             raise StopAsyncIteration
#
#         async with self.redis.client() as conn:
#             value = await conn.get(key)
#
#         return value


@asynccontextmanager
async def start_redis(url: str) -> AsyncIterator[aioredis.Redis | None]:
    redis = None
    try:
        redis = await aioredis.from_url(url)
        yield redis
    finally:
        await redis.close()


async def redis_reader(redis: aioredis.Redis, keys: iter):
    while True:
        try:
            key = next(keys)
        except StopIteration:
            break

        async with redis.client() as conn:
            value = await conn.get(key)

        yield value


async def get_redis():
    async with start_redis("redis://redis:6379") as redis:
        keys = [
            'var1',
            'var2',
            'var3',
            'var4',
        ]
        return redis_reader(redis, iter(keys))


@router.get("/")
async def start_iter(reader: AsyncIterator = Depends(get_redis)) -> None:
    # # Async for 1
    async for name in reader:
        print(name)
    #
    # # Async for 2
    # async_iter = aiter(reader)
    # while True:
    #     try:
    #         name = await anext(async_iter)
    #     except StopAsyncIteration:
    #         break
    #     else:
    #         print(name)

    # Each iteration await
