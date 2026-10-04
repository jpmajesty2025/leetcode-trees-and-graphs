'''
Given an array of non-negative integers arr, you are initially positioned at start index of the array.
When you are at index i, you can jump to i + arr[i] or i - arr[i], check if you can reach any index 
with value 0.

This module implements the in-place DFS traversal with sign-flipping.
'''


def can_reach_dfs(arr: list[int], start: int) -> bool:
    """Determine if 0 is reachable using in-place DFS sign-flipping."""
    n = len(arr)
    arr_copy = list(arr)

    def dfs(idx: int) -> bool:
        if not (0 <= idx < n) or arr_copy[idx] < 0:
            return False
        if arr_copy[idx] == 0:
            return True

        step = arr_copy[idx]
        arr_copy[idx] = -arr_copy[idx]  # Mark visited

        return dfs(idx + step) or dfs(idx - step)

    return dfs(start)


# Aliases
can_reach = can_reach_dfs
canReach = can_reach_dfs
