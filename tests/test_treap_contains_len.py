import pytest


def test_contains_operator(filled_tree, empty_tree):
    assert 10 not in empty_tree, "Empty tree should not contain any key"

    assert 10 in filled_tree, "Key 10 should be in the filled tree"
    assert 5 in filled_tree, "Key 5 should be in the filled tree"
    assert 15 in filled_tree, "Key 15 should be in the filled tree"
    assert 7 in filled_tree, "Key 7 should be in the filled tree"
    assert 12 in filled_tree, "Key 12 should be in the filled tree"
    assert 18 in filled_tree, "Key 18 should be in the filled tree"
    assert 100 not in filled_tree, "Key 100 should not be in the filled tree"


def test_len_function(filled_tree, empty_tree):
    # Проверка количества узлов в дереве
    assert len(filled_tree) == 6, "Tree should have 6 nodes"
    assert len(empty_tree) == 0, "Empty tree should have 0 nodes"
