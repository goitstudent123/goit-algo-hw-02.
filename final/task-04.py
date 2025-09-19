import uuid
import networkx as nx
import matplotlib.pyplot as plt
import heapq

def heap_tree_positions(n):
    pos = {}
    def level(i):
        l = 0
        while (1 << l) <= i:
            l += 1
        return l - 1
    for i in range(n):
        l = level(i+1)
        idx_in_level = i - ((1<<l) - 1)
        width = 2 ** l
        x = (idx_in_level + 1) / (width + 1)
        y = -l
        pos[i] = (x, y)
    return pos

def draw_heap(arr):
    G = nx.DiGraph()
    n = len(arr)
    for i in range(n):
        G.add_node(i, label=str(arr[i]))
        left = 2*i + 1
        right = 2*i + 2
        if left < n:
            G.add_edge(i, left)
        if right < n:
            G.add_edge(i, right)
    pos = heap_tree_positions(n)
    labels = {i: G.nodes[i]['label'] for i in G.nodes}
    colors = ["#87CEEB"] * n
    plt.figure(figsize=(8,5))
    nx.draw(G, pos=pos, labels=labels, arrows=False, node_size=1800, node_color=colors)
    plt.title("Binary heap visualized as a tree")
    plt.axis("off")
    plt.show()

def main():
    arr = [19, 3, 17, 10, 84, 19, 6, 22, 9]
    heapq.heapify(arr)
    print("Heap array:", arr)
    draw_heap(arr)
    print("Conclusion: a heap stored in an array maps to a complete binary tree where children of i are 2i+1 and 2i+2.")

if __name__ == "__main__":
    main()
