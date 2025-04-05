import pytest
from collections import deque
import functools
import copy
from typing import Callable, Any

from project.decorators import (
    curry_explicit,
    uncurry_explicit,
    cache_results,
    smart_args,
    Evaluated,
    Isolated,
)


def test_curry_explicit_basic():
    def add(a, b, c):
        return a + b + c

    curried = curry_explicit(add, 3)
    assert curried(1)(2)(3) == 6
    assert curried(1, 2)(3) == 6
    assert curried(1, 2, 3) == 6


def test_curry_explicit_negative_arity():
    with pytest.raises(ValueError, match="Arity cannot be negative"):
        curry_explicit(lambda x: x, -1)


def test_curry_explicit_too_many_args():
    curried = curry_explicit(lambda x, y: x + y, 2)
    with pytest.raises(ValueError, match="Too many arguments provided"):
        curried(1, 2, 3)


def test_uncurry_explicit_basic():
    def add(a):
        return lambda b: a + b

    uncurried = uncurry_explicit(add, 2)
    assert uncurried(2, 3) == 5


def test_uncurry_explicit_wrong_args():
    uncurried = uncurry_explicit(lambda x: lambda y: x + y, 2)
    with pytest.raises(ValueError, match="Incorrect number of arguments provided"):
        uncurried(1)


def test_uncurry_explicit_negative_arity():
    with pytest.raises(ValueError, match="Arity cannot be negative"):
        uncurry_explicit(lambda x: x, -1)


def test_cache_results_basic():
    call_count = 0

    @cache_results()
    def add(a, b):
        nonlocal call_count
        call_count += 1
        return a + b

    assert add(1, 2) == 3
    assert add(1, 2) == 3
    assert call_count == 1


def test_cache_results_with_size():
    call_count = 0

    @cache_results(size=1)
    def add(a, b):
        nonlocal call_count
        call_count += 1
        return a + b

    assert add(1, 2) == 3
    assert add(1, 2) == 3
    assert call_count == 1
    assert add(2, 3) == 5
    assert add(1, 2) == 3
    assert call_count == 3


def test_smart_args_basic():
    def func(a, b=1):
        return a + b

    smart = smart_args(func)
    assert smart(2) == 3
    assert smart(2, b=2) == 4


def test_smart_args_evaluated():
    call_count = 0

    def get_value():
        nonlocal call_count
        call_count += 1
        return 5

    def func(a, b=Evaluated(get_value)):
        return a + b

    smart = smart_args(func)
    assert smart(3) == 8
    assert call_count == 1
    assert smart(3) == 8
    assert call_count == 2  # Evaluated вызывается каждый раз


def test_smart_args_isolated():
    def func(a, b=Isolated()):
        b.append(1)
        return a, b

    smart = smart_args(func)
    lst = [0]
    result1 = smart(5, lst)
    result2 = smart(5, lst)
    assert result1 == (5, [0, 1])
    assert result2 == (5, [0, 1])
    assert lst == [0]  # Исходный список не изменился
