import pytest


def test_delete_item(filled_tree):
    # Проверка удаления узла
    filled_tree.__delitem__(5)
    with pytest.raises(KeyError):
        _ = filled_tree[5]
    assert filled_tree[10] == 100, "Root node with key 10 should still exist"
