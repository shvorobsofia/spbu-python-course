import pytest


def test_heap_property(filled_tree):
    # Проверка свойства кучи (value родителя > value детей) для Treap
    def check_heap_property(node):
        if node is None:
            return True
        if node.left and node.left.value > node.value:
            return False
        if node.right and node.right.value > node.value:
            return False
        return check_heap_property(node.left) and check_heap_property(node.right)

    assert check_heap_property(
        filled_tree.root
    ), "Heap property (parent value > children values) should hold for all nodes"
