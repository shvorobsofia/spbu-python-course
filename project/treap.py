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

    def __getitem__(self, key):
        node = self.find(self.root, key)
        if node is not None:
            return node.value
        raise KeyError(f"Key {key} not found in Treap")

    def __setitem__(self, key, value):
        self.insert_node(key, value)

    def __delitem__(self, key):
        self.root = self.remove(self.root, key)

    def __iter__(self):
        return self.inorder(self.root)

    def __len__(self):
        return self.count_nodes(self.root)


    def inorder(self, node):
        if node is not None:
            yield from self.inorder(node.left)
            yield node.key
            yield from self.inorder(node.right)

    def count_nodes(self, node):
        if node is None:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    def preorder(self, root: TreapNode):
        if root is None:
            return
        print(root.key, end=" ")
        self.preorder(root.left)
        self.preorder(root.right)

    def postorder(self, root: TreapNode):
        if root is None:
            return
        self.preorder(root.left)
        self.preorder(root.right)
        print(root.key, end=" ")

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
        if root is None:
            return None
        elif root.key < key:
            root.right = self.remove(root.right, key)
        elif root.key > key:
            root.left = self.remove(root.left, key)
        else:
            root = self.merge(root.left, root.right)
        return root

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

    def find(self, root: TreapNode, key):
        if root is None:
            return None
        elif root.key < key:
            root.right = self.find(root.right, key)
        elif root.key > key:
            root.left = self.find(root.left, key)
        else:
            return root
