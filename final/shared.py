from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Iterable, Tuple, Dict, List
import math

# Singly linked list basics
@dataclass
class Node:
    value: int
    next: Optional["Node"] = None

class LinkedList:
    def __init__(self, values: Optional[Iterable[int]] = None):
        self.head: Optional[Node] = None
        if values:
            for v in reversed(list(values)):
                self.push_front(v)

    def push_front(self, value: int) -> None:
        self.head = Node(value, self.head)

    def to_list(self) -> list:
        out = []
        cur = self.head
        while cur:
            out.append(cur.value)
            cur = cur.next
        return out

    def reverse(self) -> None:
        prev = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    def insertion_sort(self) -> None:
        sorted_head = None
        cur = self.head
        while cur:
            nxt = cur.next
            sorted_head = _sorted_insert(sorted_head, cur)
            cur = nxt
        self.head = sorted_head

def _sorted_insert(head: Optional[Node], node: Node) -> Optional[Node]:
    if head is None or node.value < head.value:
        node.next = head
        return node
    cur = head
    while cur.next and cur.next.value <= node.value:
        cur = cur.next
    node.next = cur.next
    cur.next = node
    return head

def merge_sorted(a: Optional[Node], b: Optional[Node]) -> Optional[Node]:
    dummy = Node(0)
    tail = dummy
    while a and b:
        if a.value <= b.value:
            tail.next, a = a, a.next
        else:
            tail.next, b = b, b.next
        tail = tail.next
    tail.next = a if a else b
    return dummy.next

# Color utilities
def gradient_hex(n: int, dark: Tuple[int,int,int]=(30,30,120), light: Tuple[int,int,int]=(180,220,255)) -> List[str]:
    if n <= 0:
        return []
    def interp(c1, c2, t):
        return int(round(c1 + (c2 - c1) * t))
    out = []
    for i in range(n):
        t = 0 if n == 1 else i / (n - 1)
        r = interp(dark[0], light[0], t)
        g = interp(dark[1], light[1], t)
        b = interp(dark[2], light[2], t)
        out.append(f"#{r:02X}{g:02X}{b:02X}")
    return out
