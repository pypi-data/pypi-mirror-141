from typing import Tuple


def manhattan(p1: Tuple[int, ...], p2: Tuple[int, ...]) -> int:
    """Calculate Manhattan distance between two points."""
    return sum(abs(v1 - v2) for v1, v2 in zip(p1, p2))
