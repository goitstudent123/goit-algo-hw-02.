# Find minimum in BST/AVL; exports ROOT and MIN_VALUE for the next task.

from typing import Optional
from common import Node, build_demo_bst, print_tree


def find_min_node(root: Optional[Node]) -> Optional[Node]:
    """Return the node with the smallest key or None if the tree is empty."""
    if root is None:
        return None
    curr = root
    # Go left until the last left child
    while curr.left is not None:
        curr = curr.left
    return curr


def find_min_value(root: Optional[Node]):
    """Return the smallest key value or raise an error if the tree is empty."""
    node = find_min_node(root)
    if node is None:
        raise ValueError("Tree is empty, minimum not found")
    return node.key


ROOT: Node = build_demo_bst()
MIN_VALUE = find_min_value(ROOT)

if __name__ == "__main__":
    print_tree(ROOT)
    print("Min value:", MIN_VALUE)  # Expected: 1
