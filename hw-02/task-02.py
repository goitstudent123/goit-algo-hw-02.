#!/usr/bin/env python3
"""Task 2: Palindrome check using deque.

- Case-insensitive
- Whitespace-insensitive (spaces, tabs, newlines are ignored)
- Uses collections.deque for O(1) pops from both ends
"""

from collections import deque
from typing import Iterable


def is_palindrome(text: str) -> bool:
    """Return True if `text` is a palindrome (ignoring case and whitespace).

    The function normalizes the input by:
      - converting to lowercase
      - removing all whitespace characters (spaces, tabs, newlines, etc.)

    It then loads characters into a deque and compares both ends until the deque
    has length < 2.

    Example:
        >>> is_palindrome("Never odd or even")
        True
        >>> is_palindrome("Hello")
        False
    """
    # Normalize: lowercase and strip whitespace characters
    cleaned = (c.lower() for c in text if not c.isspace())

    d = deque(cleaned)
    while len(d) > 1:
        if d.popleft() != d.pop():
            return False
    return True


def _demo(samples: Iterable[str]) -> None:
    for s in samples:
        print(f"{s!r} -> {is_palindrome(s)}")


if __name__ == "__main__":
    _demo([
        "Never odd or even",
        "Я несу гусеня",
        "A man a plan a canal Panama",
        "Hello, World!",
        "12321",
        "123 321",
    ])
