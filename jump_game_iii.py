'''
Given an array of non-negative integers arr, you are initially positioned at start index of the array.
When you are at index i, you can jump to i + arr[i] or i - arr[i], check if you can reach any index 
with value 0.

Notice that you can not jump outside of the array at any time.
'''

from collections import deque


def can_reach(arr: list[int], start: int) -> bool:
    """Determine if we can reach an index with value 0 using BFS with deque."""
    n = len(arr)
    if not (0 <= start < n):
        return False
    if arr[start] == 0:
        return True

    queue: deque[int] = deque([start])
    visited: set[int] = {start}

    while queue:
        curr = queue.popleft()
        if arr[curr] == 0:
            return True

        for next_idx in (curr + arr[curr], curr - arr[curr]):
            if 0 <= next_idx < n and next_idx not in visited:
                visited.add(next_idx)
                queue.append(next_idx)

    return False


# LeetCode backward compatibility aliases
canReach = can_reach
