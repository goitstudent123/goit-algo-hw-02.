# task3.py

from typing import List, Tuple
import heapq
import task2

def min_merge_cost(cables: List[int]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """
    Return minimal total cost to connect all cables and the merge order.
    Each merge step is recorded as (a, b, a_plus_b), where a <= b.

    Edge cases:
      - []  -> cost 0, no merges
      - [x] -> cost 0, no merges (already one cable)
    """
    if not cables or len(cables) == 1:
        return 0, []

    heap = list(cables)
    heapq.heapify(heap)

    total_cost = 0
    merges: List[Tuple[int, int, int]] = []

    # Always merge the two smallest cables first
    while len(heap) > 1:
        a = heapq.heappop(heap)  # smallest
        b = heapq.heappop(heap)  # second smallest
        c = a + b  # cost for this merge equals new cable length
        total_cost += c
        merges.append((a, b, c))  # record the merge step
        heapq.heappush(heap, c)  # push the new combined cable back

    return total_cost, merges


if __name__ == "__main__":
    cables = task2.CABLES_FROM_TREE  # e.g., [1, 2, 3, 5, 7, 10, 14]
    cost, order = min_merge_cost(cables)
    print("Cables:", cables)
    print("Minimal total cost:", cost)
    print("Merge order (a, b -> a+b):")
    for a, b, c in order:
        print(f"{a} + {b} -> {c}")
