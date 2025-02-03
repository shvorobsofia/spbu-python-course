import functools
import copy
from collections import deque
from typing import Callable, Any


def curry_explicit(function: Callable, arity: int) -> Callable:
    if arity < 0:
        raise ValueError("Arity cannot be negative")

    def curried(*args):
        if len(args) > arity:
            raise ValueError("Too many arguments provided")
        if len(args) == arity:
            return function(*args)
        return lambda *next_args: curried(*(args + next_args))

    return curried


def uncurry_explicit(function: Callable, arity: int) -> Callable:
    if arity < 0:
        raise ValueError("Arity cannot be negative")

    def uncurried(*args):
        if len(args) != arity:
            raise ValueError("Incorrect number of arguments provided")
        result = function
        for arg in args:
            result = result(arg)
        return result

    return uncurried


def cache_results(size: int = 0):
    def decorator(func: Callable):
        cache = {}
        order = deque()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            if size > 0:
                if len(order) >= size:
                    oldest_key = order.popleft()
                    cache.pop(oldest_key, None)
                cache[key] = result
                order.append(key)
            return result

        return wrapper

    return decorator


class Evaluated:
    def __init__(self, func: Callable[[], Any]):
        self.func = func

    def __call__(self):
        return self.func()


class Isolated:
    pass

def smart_args(func: Callable) -> Callable:
    defaults = func.__defaults__ or ()
    default_dict = {}

    for i, param in enumerate(func.__code__.co_varnames[:func.__code__.co_argcount]):
        if i < len(defaults):
            default_dict[param] = defaults[i]

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_kwargs = {}
        for key, value in kwargs.items():
            if isinstance(default_dict.get(key, None), Evaluated):
                new_kwargs[key] = default_dict[key]()
            elif isinstance(default_dict.get(key, None), Isolated):
                new_kwargs[key] = copy.deepcopy(value)
            else:
                new_kwargs[key] = value
        return func(*args, **new_kwargs)

    return wrapper
