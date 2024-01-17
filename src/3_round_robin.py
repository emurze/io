import itertools as it
from collections.abc import Iterator

gen1 = it.chain('LERA')
gen2 = it.chain(range(4))


def round_robin(tasks: list[Iterator]):
    while tasks:
        task = tasks.pop(0)

        try:
            res = next(task)
            print(res)
            tasks.append(task)
        except StopIteration:
            pass


if __name__ == '__main__':
    round_robin([gen1, gen2])  # state objects
