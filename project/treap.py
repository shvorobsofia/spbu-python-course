from collections.abc import MutableMapping


class TreapNode:
    key = None
    value = None
    left = None
    right = None

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Treap(MutableMapping):
    def __init__(self):
        self.root = None

    def insert_node(self, key, value):

        new_node = TreapNode.__init__(key, value)
        if self.root is None:
            self.root = new_node
            return
        else:
            left, right = self.split(self.root, key - 1)
            self.root = self.merge(left, new_node)
            self.root = self.merge(self.root, right)


    def remove(self, root: TreapNode, key):
        

    def split(self, root: TreapNode, key):
        if root is None:
            return None, None
        elif root.key < key:
            (left, right) = self.split(root.right, key)
            root.right = left
            return root, right
        else:
            (left, right) = self.split(root.left, key)
            root.left = right
            return left, root

    def merge(self, left: TreapNode, right: TreapNode):
        if left is None:
            return right
        if right is None:
            return left
        elif left.value > right.value:
            left.right = self.merge(left.right, right)
            return left
        else:
            right.left = self.merge(right.left, left)
            return right
