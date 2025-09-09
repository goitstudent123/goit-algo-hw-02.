# Sum all values in the tree; derives cable lengths from the tree for task3.

from typing import Optional, List
from common import Node
import task1

ROOT: Node = task1.ROOT

def sum_tree_recursive(root: Optional[Node]) -> int:
    """Return the sum of all node keys using recursive DFS."""
    if root is None:
        return 0
    # sum = current key + sum(left subtree) + sum(right subtree)
    return root.key + sum_tree_recursive(root.left) + sum_tree_recursive(root.right)


def sum_tree_iterative_dfs(root: Optional[Node]) -> int:
    """Return the sum using iterative DFS (explicit stack)."""
    if root is None:
        return 0
    total = 0
    stack: List[Node] = [root]
    while stack:
        node = stack.pop()
        total += node.key
        # Push children; order does not matter for sum
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return total


def inorder_values(root: Optional[Node]) -> List[int]:
    """Return an in-order list of keys (sorted for BST)."""
    out: List[int] = []
    stack: List[Node] = []
    curr = root
    while curr is not None or stack:
        while curr is not None:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        out.append(curr.key)
        curr = curr.right
    return out


# Compute sums (exported so task3 can import this module and it will run)
SUM_RECURSIVE = sum_tree_recursive(ROOT)
SUM_ITER_DFS = sum_tree_iterative_dfs(ROOT)

# For task3, we need to derive cable lengths from the tree
CABLES_FROM_TREE: List[int] = inorder_values(ROOT)

if __name__ == "__main__":
    print("Sum recursive:", SUM_RECURSIVE)     # Expected: 42
    print("Sum iterative DFS:", SUM_ITER_DFS)  # Expected: 42
    print("Cables (from inorder):", CABLES_FROM_TREE)  # Expected: [1,2,3,5,7,10,14]
