import pytest


def test_insert_and_get_item(empty_tree):
    # Проверка вставки и получения значения
    empty_tree[10] = 100
    empty_tree[5] = 80
    assert empty_tree[10] == 100, "Value for key 10 should be 100"
    assert empty_tree[5] == 80, "Value for key 5 should be 80"


def test_get_nonexistent_key(empty_tree):
    with pytest.raises(KeyError):
        _ = empty_tree[100]
