import pytest


def test_inorder_key_bst(filled_tree):
    expected_list = [5, 7, 10, 12, 15, 18]
    assert expected_list == list(filled_tree.inorder(filled_tree.root))


def test_inorder_traversal(filled_tree):
    # Проверка обхода inorder
    expected_inorder = [5, 7, 10, 12, 15, 18]
    assert (
        list(filled_tree.inorder(filled_tree.root)) == expected_inorder
    ), "Inorder traversal does not match expected output"


def test_preorder_traversal(filled_tree):
    expected_preorder = [10, 7, 5, 12, 15, 18]
    assert list(filled_tree.preorder(filled_tree.root)) == expected_preorder


def test_postorder_traversal(filled_tree):
    expected_postorder = [5, 7, 18, 15, 12, 10]
    assert list(filled_tree.postorder(filled_tree.root)) == expected_postorder
