import heapq
from typing import Dict, List, Tuple

class Graph:
    def __init__(self):
        self.adj: Dict[str, List[Tuple[str, int]]] = {}

    def add_edge(self, u: str, v: str, w: int):
        self.adj.setdefault(u, []).append((v, w))
        self.adj.setdefault(v, [])  # ensure presence

    def dijkstra(self, start: str) -> Tuple[Dict[str, int], Dict[str, str]]:
        dist = {v: float('inf') for v in self.adj}
        prev: Dict[str, str] = {}
        dist[start] = 0
        pq = [(0, start)]
        visited = set()
        while pq:
            d, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            for v, w in self.adj.get(u, []):
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    prev[v] = u
                    heapq.heappush(pq, (nd, v))
        return dist, prev

def main():
    g = Graph()
    edges = [
        ("A","B",4), ("A","C",2), ("B","C",5), ("B","D",10),
        ("C","E",3), ("E","D",4), ("D","F",11)
    ]
    for u,v,w in edges:
        g.add_edge(u,v,w)
    dist, prev = g.dijkstra("A")
    print("Distances:", dist)
    print("Parents:", prev)
    print("Conclusion: using a binary heap keeps selection of the next closest vertex efficient (O((V+E) log V)).")

if __name__ == "__main__":
    main()
