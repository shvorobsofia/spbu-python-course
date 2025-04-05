import functools
import copy
from collections import deque
from typing import Any, Callable, Deque, Dict


def curry_explicit(function: Callable, arity: int) -> Callable:
    """
    Каррирует функцию с явно заданной арностью.
    Параметры:
        function: исходная функция для каррирования
        arity: количество аргументов для полного применения
    Возвращает:
        Каррированную функцию
    Исключения:
        ValueError при отрицательной arity или избыточном количестве аргументов
    """
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
    """
    Обратное преобразование каррированной функции.
    Параметры:
        function: каррированная функция
        arity: количество аргументов для полного применения
    Возвращает:
        Обычную функцию с фиксированным количеством аргументов
    Исключения:
        ValueError при отрицательной arity или неверном количестве аргументов
    """
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
    """
    Декоратор для кэширования результатов вызовов функции.
    Параметры:
        size: максимальный размер кэша (0 = без ограничений)
    Особенности:
        - Использует LRU стратегию при size > 0
        - Ключ формируется из позиционных и именованных аргументов
    """

    def decorator(func: Callable):
        cache: Dict[Any, Any] = {}
        order: Deque[Any] = deque()

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (args, frozenset(kwargs.items()))
            if key in cache:
                return cache[key]
            result = func(*args, **kwargs)
            cache[key] = result
            if size > 0:
                if len(order) >= size:
                    oldest_key = order.popleft()
                    del cache[oldest_key]
                order.append(key)
            return result

        return wrapper

    return decorator


class Evaluated:
    """
    Класс для отложенного вычисления значений по умолчанию.
    При вызове возвращает результат обернутой функции.
    """

    def __init__(self, func: Callable[[], Any]):
        self.func = func

    def __call__(self):
        return self.func()


class Isolated:
    """
    Маркер для изолированных значений по умолчанию.
    Гарантирует глубокое копирование аргументов при каждом вызове.
    """


def smart_args(func: Callable) -> Callable:
    """
    Умный обработчик аргументов функции с расширенными возможностями:
    - Автоматическое копирование объектов, помеченных Isolated
    - Ленивые вычисления значений, обернутых в Evaluated
    - Сохранение сигнатуры исходной функции
    """
    defaults = func.__defaults__ or ()
    param_names = func.__code__.co_varnames[: func.__code__.co_argcount]
    default_dict = dict(zip(param_names[-len(defaults) :], defaults))

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        new_kwargs = kwargs.copy()
        sig = func.__code__.co_varnames[: func.__code__.co_argcount]
        args_dict = dict(zip(sig, args))

        for param in sig:
            if param in args_dict:
                default_value = default_dict.get(param)
                if isinstance(default_value, Isolated):
                    new_kwargs[param] = copy.deepcopy(args_dict[param])
                else:
                    new_kwargs[param] = args_dict[param]
            elif param in new_kwargs:
                default_value = default_dict.get(param)
                if isinstance(default_value, Isolated):
                    new_kwargs[param] = copy.deepcopy(new_kwargs[param])
                elif isinstance(new_kwargs[param], Evaluated):
                    new_kwargs[param] = new_kwargs[param]()
            elif param in default_dict:
                default_value = default_dict[param]
                if isinstance(default_value, Evaluated):
                    new_kwargs[param] = default_value()
                elif isinstance(default_value, Isolated):
                    new_kwargs[param] = []
                else:
                    new_kwargs[param] = default_value

        return func(**new_kwargs)

    return wrapper
