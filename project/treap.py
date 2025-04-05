from collections.abc import MutableMapping
from typing import Optional


class TreapNode:
    """A node in the Treap data structure.

    A TreapNode represents a single node in the Treap, which combines properties
    of a binary search tree (BST) and a heap. Each node stores a key, a value, and
    references to its left and right children.

    Attributes:
        key: The key of the node, used for BST ordering.
        value: The value associated with the key, used for heap ordering.
        left (Optional[TreapNode]): The left child of the node, or None.
        right (Optional[TreapNode]): The right child of the node, or None.
    """

    key = None
    value = None
    left = None
    right = None


    def __init__(self, key, value):
        """Initialize a new TreapNode with a key and value.

        Args:
            key: The key of the node, used for BST ordering.
            value: The value of the node, used for heap ordering.
        """
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class Treap(MutableMapping):
    """A Treap data structure that combines a binary search tree and a heap.

    The Treap (Tree + Heap) is a randomized self-balancing binary search tree where
    each node has a key and a value. The keys maintain BST properties (left subtree
    keys are less than the node's key, right subtree keys are greater), and the values
    maintain heap properties (a parent's value is greater than its children's values).
    This implementation inherits from MutableMapping, providing dictionary-like
    functionality.

    Attributes:
        root (Optional[TreapNode]): The root node of the Treap, or None if the Treap
            is empty.
    """
    def __init__(self):
        """Initialize an empty Treap."""
        self.root = None

    def __getitem__(self, key):
        """Retrieve the value associated with the given key.

        Args:
            key: The key to look up in the Treap.

        Returns:
            The value associated with the key.

        Raises:
            KeyError: If the key is not found in the Treap.
        """
        node = self.find(self.root, key)
        if node is not None:
            return node.value
        raise KeyError(f"Key {key} not found in Treap")

    def __setitem__(self, key, value):
        """Insert or update a key-value pair in the Treap.

        Args:
            key: The key to insert or update.
            value: The value to associate with the key.
        """
        self.insert_node(key, value)

    def __delitem__(self, key):
        """Remove a key-value pair from the Treap.

        Args:
            key: The key to remove.

        Raises:
            KeyError: If the key is not found in the Treap.
        """
        self.root = self.remove(self.root, key)

    def __iter__(self):
        """Return an iterator over the keys in the Treap.

        The keys are returned in sorted order (inorder traversal).

        Returns:
            An iterator yielding the keys in the Treap.
        """
        return self.inorder(self.root)

    def __len__(self):
        """Return the number of nodes in the Treap.

        Returns:
            int: The number of key-value pairs in the Treap.
        """
        return self.count_nodes(self.root)

    def inorder(self, node):
        """Perform an inorder traversal of the Treap starting from the given node.

        Args:
            node: The root node of the subtree to traverse, or None.

        Yields:
            The keys of the nodes in inorder (sorted) order.
        """
        if node is not None:
            yield from self.inorder(node.left)
            yield node.key
            yield from self.inorder(node.right)

    def count_nodes(self, node):
        """Count the number of nodes in the subtree rooted at the given node.

        Args:
            node: The root node of the subtree to count, or None.

        Returns:
            int: The number of nodes in the subtree.
        """
        if node is None:
            return 0
        return 1 + self.count_nodes(node.left) + self.count_nodes(node.right)

    def preorder(self, node: Optional[TreapNode]):
        """Perform a preorder traversal of the Treap starting from the given node.

        Args:
            node: The root node of the subtree to traverse, or None.

        Yields:
            The keys of the nodes in preorder (root, left, right) order.
        """
        if node is not None:
            yield node.key
            yield from self.preorder(node.left)
            yield from self.preorder(node.right)

    def postorder(self, node: Optional[TreapNode]):
        """Perform a postorder traversal of the Treap starting from the given node.

        Args:
            node: The root node of the subtree to traverse, or None.

        Yields:
            The keys of the nodes in postorder (left, right, root) order.
        """
        if node is not None:
            yield from self.postorder(node.left)
            yield from self.postorder(node.right)
            yield node.key

    def insert_node(self, key, value):
        """Insert a new key-value pair into the Treap.

        Args:
            key: The key to insert.
            value: The value to associate with the key.
        """
        new_node = TreapNode(key, value)
        if self.root is None:
            self.root = new_node
            return
        else:
            left, right = self.split(self.root, key)
            self.root = self.merge(left, new_node)
            self.root = self.merge(self.root, right)

    def remove(self, root: Optional[TreapNode], key):
        """Remove a node with the given key from the subtree.

        Args:
            root: The root node of the subtree to remove from, or None.
            key: The key to remove.

        Returns:
            Optional[TreapNode]: The new root of the subtree after removal, or None
                if the subtree is empty.

        Raises:
            KeyError: If the key is not found in the Treap.
        """
        if root is None:
            return None
        elif root.key < key:
            root.right = self.remove(root.right, key)
        elif root.key > key:
            root.left = self.remove(root.left, key)
        else:
            root = self.merge(root.left, root.right)
        return root

    def split(self, root: Optional[TreapNode], key):
        """Split the Treap into two subtrees based on the given key.

        Args:
            root: The root node of the subtree to split, or None.
            key: The key to split on.

        Returns:
            Tuple[Optional[TreapNode], Optional[TreapNode]]: A tuple of two subtrees:
                - The left subtree contains all nodes with keys less than the given key.
                - The right subtree contains all nodes with keys greater than or equal
                  to the given key.
        """
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

    def merge(self, left: Optional[TreapNode], right: Optional[TreapNode]):
        """Merge two Treaps into one while maintaining BST and heap properties.

        Args:
            left: The root of the left Treap, or None.
            right: The root of the right Treap, or None.

        Returns:
            Optional[TreapNode]: The root of the merged Treap, or None if both inputs
                are None.

        Notes:
            Assumes that all keys in the left Treap are less than all keys in the right
            Treap. The heap property is maintained by comparing the values of the nodes.
        """
        if left is None:
            return right
        elif right is None:
            return left
        else:
            if (left.value is None) | (right.value is None):
                return None

            assert left.value is not None
            assert right.value is not None

            if left.value > right.value:
                left.right = self.merge(left.right, right)
                return left
            else:
                right.left = self.merge(right.left, left)
                return right

    def find(self, root: Optional[TreapNode], key):
        """Find a node with the given key in the subtree.

        Args:
            root: The root node of the subtree to search in, or None.
            key: The key to search for.

        Returns:
            Optional[TreapNode]: The node with the given key, or None if the key is not
                found.
        """
        if root is None:
            return None
        elif root.key < key:
            return self.find(root.right, key)
        elif root.key > key:
            return self.find(root.left, key)
        return root
