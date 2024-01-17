

```python
class Sentence:
    """
    Iterable is object that can be iterated over
    """

    def __init__(self, text: str) -> None:
        self.text = text
        self.words = text.split(' ')

    def __iter__(self) -> Iterator:
        return SentenceIterator(self.words)


class SentenceIterator:
    """
    Iterator is object that implements __iter__ and __next__
    """

    def __init__(self, words: list[str]) -> None:
        self.words = words
        self.index = 0

    def __next__(self) -> str:
        try:
            word = self.words[self.index]
        except IndexError:
            raise StopIteration
        self.index += 1
        return word

    def __iter__(self) -> Iterator:
        return self
```

```python magic
from collections.abc import Generator, Callable


class Averager3:
    count = 0
    total = 0

    def __call__(self, item: float) -> float:
        self.total += item
        self.count += 1
        return self.total / self.count


def averager2() -> Callable:
    count = 0
    total = 0

    def inner(item) -> float:
        nonlocal count, total
        total += item
        count += 1
        return total / count

    return inner


def averager() -> Generator[float, float, None]:
    count = 0
    total = 0
    average = 0
    while True:
        item = yield average
        total += item
        count += 1
        average = total / count


def get_avg3() -> Callable:
    return Averager3()


def get_avg2() -> Callable:
    return averager2()


def get_avg() -> Callable:
    avg = averager()
    next(avg)
    return avg.send


def main(avg) -> None:
    assert avg(1) == 1.0
    assert avg(53) == 27.0
    assert avg(3) == 19.0
    assert avg(24) == 20.25


if __name__ == '__main__':
    main(get_avg())
    main(get_avg2())
    main(get_avg3())

```