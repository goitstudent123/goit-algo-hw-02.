# common.py
# Shared structures and helpers (Python 3.9 compatible; comments in English)

from typing import Optional


class Node:
    def __init__(self, key, left: Optional["Node"] = None, right: Optional["Node"] = None, height: int = 1):
        self.key = key
        self.left = left
        self.right = right
        # 'height' is used by AVL; harmless for plain BST
        self.height = height


def bst_insert(root: Optional[Node], key) -> Node:
    """Insert key into a BST (duplicates ignored for simplicity)."""
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = bst_insert(root.left, key)
    elif key > root.key:
        root.right = bst_insert(root.right, key)
    return root


def build_demo_bst() -> Node:
    """Build and return a small sample BST to drive all tasks."""
    root: Optional[Node] = None
    for x in [10, 5, 14, 2, 7, 1, 3]:
        root = bst_insert(root, x)
    return root

def print_tree(root: Optional[Node], level: int = 0, prefix: str = "Root: "):
    """Pretty-print the tree sideways in the console."""
    if root is not None:
        # Print right subtree first (so it appears at the top)
        print_tree(root.right, level + 1, "R--- ")
        # Print current node
        print("    " * level + prefix + str(root.key))
        # Print left subtree
        print_tree(root.left, level + 1, "L--- ")
