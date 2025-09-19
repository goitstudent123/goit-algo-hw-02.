import networkx as nx
import matplotlib.pyplot as plt
from shared import gradient_hex

class BNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def build_example_tree():
    root = BNode(3)

    root.left = BNode(9)
    root.right = BNode(6)

    root.left.left = BNode(10)
    root.left.right = BNode(84)
    root.right.left = BNode(19)
    root.right.right = BNode(17)

    root.left.left.left = BNode(22)
    root.left.left.right = BNode(21)

    return root

def to_graph(root):
    G = nx.DiGraph()
    nodes = []
    q = [(root, 0)]
    while q:
        node, idx = q.pop(0)
        nodes.append((node, idx))
        G.add_node(idx, label=str(node.val))
        if node.left:
            li = len(nodes) + len(q) + 1
            q.append((node.left, li))
            G.add_edge(idx, li)
        if node.right:
            ri = len(nodes) + len(q) + 1
            q.append((node.right, ri))
            G.add_edge(idx, ri)
    return G

def layout_complete(G):
    n = len(G.nodes)
    pos = {}
    def level(i):
        l = 0
        while (1 << l) <= i+1:
            l += 1
        return l - 1
    for i in G.nodes:
        l = level(i)
        idx_in_level = i - ((1<<l) - 1)
        width = 2 ** l
        x = (idx_in_level + 1) / (width + 1)
        y = -l
        pos[i] = (x, y)
    return pos

def bfs_order(root):
    order = []
    q = [root]
    while q:
        node = q.pop(0)
        order.append(node.val)
        if node.left:
            q.append(node.left)
        if node.right:
            q.append(node.right)
    return order

def dfs_order(root):
    order = []
    stack = [root]
    while stack:
        node = stack.pop()
        order.append(node.val)
        if node.right:
            stack.append(node.right)
        if node.left:
            stack.append(node.left)
    return order

def color_by_order(G, mapping):
    labels = nx.get_node_attributes(G, "label")
    values = [int(labels[i]) for i in G.nodes]
    order_indices = {v: idx for idx, v in enumerate(mapping)}
    idxs = [order_indices.get(v, 0) for v in values]
    colors = gradient_hex(len(G.nodes))
    node_colors = [colors[i] for i in idxs]
    return node_colors

def draw_with_colors(G, node_colors, title):
    pos = layout_complete(G)
    labels = {i: G.nodes[i]['label'] for i in G.nodes}
    plt.figure(figsize=(8,5))
    nx.draw(G, pos=pos, labels=labels, arrows=False, node_size=1800, node_color=node_colors)
    plt.title(title)
    plt.axis("off")
    plt.show()

def main():
    root = build_example_tree()
    G = to_graph(root)

    order_bfs = bfs_order(root)
    order_dfs = dfs_order(root)
    colors_bfs = color_by_order(G, order_bfs)
    colors_dfs = color_by_order(G, order_dfs)

    draw_with_colors(G, colors_bfs, "BFS order: dark -> light")
    draw_with_colors(G, colors_dfs, "DFS (preorder) order: dark -> light")

    print("BFS order:", order_bfs)
    print("DFS order:", order_dfs)
    print("Conclusion: BFS colors nodes level-by-level; DFS colors nodes following a stack-based preorder without recursion.")

if __name__ == "__main__":
    main()
