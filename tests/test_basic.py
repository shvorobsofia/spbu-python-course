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


def test_inorder_key_bst(filled_tree):
    expected_list = [5, 7, 10, 12, 15, 18]
    assert expected_list == list(filled_tree.inorder(filled_tree.root))


def test_insert_and_get_item(empty_tree):
    # Проверка вставки и получения значения
    empty_tree[10] = 100
    empty_tree[5] = 80
    assert empty_tree[10] == 100, "Value for key 10 should be 100"
    assert empty_tree[5] == 80, "Value for key 5 should be 80"


def test_get_nonexistent_key(empty_tree):
    with pytest.raises(KeyError):
        _ = empty_tree[100]


def test_delete_item(filled_tree):
    # Проверка удаления узла
    filled_tree.__delitem__(5)
    with pytest.raises(KeyError):
        _ = filled_tree[5]
    assert filled_tree[10] == 100, "Root node with key 10 should still exist"


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


def test_len_function(filled_tree, empty_tree):
    # Проверка количества узлов в дереве
    assert len(filled_tree) == 6, "Tree should have 6 nodes"
    assert len(empty_tree) == 0, "Empty tree should have 0 nodes"


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
