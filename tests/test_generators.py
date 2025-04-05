from itertools import product

import pytest

from project.generators import get_rgba, get_prime


@pytest.mark.parametrize(
    "index, expected",
    [
    (0, (0, 0, 0, 0)),
    (1, (0, 0, 0, 2)),
    (10, (0, 0, 0, 20)),
    (255, (0, 0, 5, 0)),
    ],
)
def test_rgba(index, expected):
    assert get_rgba(index) == expected


@pytest.mark.parametrize("k, expected", [(1, 2),(2, 3),(3, 5),(10, 29),(20, 71)])
def test_prime(k, expected):
    assert get_prime(k) == expected


def test_rgba_out_of_range():
    with pytest.raises(IndexError):
        get_rgba(10**8)


def test_prime_invalid_index():
    with pytest.raises(ValueError):
        get_prime(0)
