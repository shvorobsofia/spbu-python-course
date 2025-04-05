from itertools import product
from typing import Generator, Callable, List


def get_rgba_element(index: int):
    """Генераторное выражение для четырехмерного набора векторов RGBA, где A - четное."""
    rgba_space = ((r, g, b, a) for r, g, b, a in product(range(256), range(256), range(256), range(0, 101, 2)))

    for i, value in enumerate(rgba_space):
        if i == index:
            return value
    raise IndexError("Index out of range")


def prime_generator() -> Generator[int, None, None]:
    """Генератор простых чисел."""
    primes: List[int] = []
    num = 2
    while True:
        if all(num % p != 0 for p in primes):
            primes.append(num)
            yield num
        num += 1


def prime_decorator(gen: Callable[[], Generator[int, None, None]]) -> Callable[[int], int]:
    """Декоратор, превращающий генератор в функцию, возвращающую k-е простое число."""
    cache: List[int] = []
    generator = gen()

    def wrapper(k: int) -> int:
        if k < 1:
            raise ValueError("Index must be greater than or equal to 1")
        while len(cache) < k:
            cache.append(next(generator))
        return cache[k - 1]

    return wrapper


def get_rgba(index: int):
    return get_rgba_element(index)


@prime_decorator
def get_prime():
    return prime_generator()