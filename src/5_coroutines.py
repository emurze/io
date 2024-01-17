import functools
from collections.abc import Coroutine, Generator, Callable
from typing import Any


def initializer(func: Callable) -> Callable:
    @functools.wraps(func)
    def inner(*args: Any, **kwargs: Any) -> Coroutine:
        _gen = func(*args, **kwargs)
        _gen.send(None)
        return _gen
    return inner


def gen() -> Generator[None, int, float]:
    total = 0
    while True:
        try:
            num = yield
            total += num
        except StopIteration:
            break
    return total


@initializer
def run() -> Coroutine:
    result = yield from gen()
    # main aim is to return control flow to event_loop

    print(result)

    result2 = yield from 'wefwef'

    print(result2)


def event_loop(cor: Coroutine) -> None:
    cor.send(0)
    cor.send(64)
    cor.send(5)
    cor.throw(StopIteration)
    cor.send(None)
    cor.send(None)
    cor.send(None)
    cor.send(None)
    cor.send(None)
    cor.throw(StopIteration)


if __name__ == '__main__':
    event_loop(run())
