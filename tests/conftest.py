import pytest

from project.treap import Treap, TreapNode


@pytest.fixture
def empty_tree():
    return Treap()


@pytest.fixture
def filled_tree():
    tree = Treap()
    # Добавляем узлы, чтобы значения value у родителя всегда были больше значений детей
    tree.insert_node(10, 100)
    tree.insert_node(5, 80)
    tree.insert_node(15, 60)
    tree.insert_node(7, 90)
    tree.insert_node(12, 70)
    tree.insert_node(18, 50)
    return tree
