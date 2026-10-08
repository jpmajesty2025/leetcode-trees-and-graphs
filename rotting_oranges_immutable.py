'''
Calculate the minimum minutes for all fresh oranges to rot using Multi-Source BFS.
Non-destructive: preserves the original input grid by tracking visited / rot times.
'''

from collections import deque
from typing import List


def oranges_rotting_immutable(grid: List[List[int]]) -> int:
    """Multi-source BFS without mutating the input grid.

    Time Complexity: O(M * N) where M is rows and N is columns.
    Space Complexity: O(M * N) for the visited set and queue.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh_set = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh_set.add((r, c))

    if not fresh_set:
        return 0

    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    minutes_passed = 0

    while queue and fresh_set:
        minutes_passed += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                neighbor = (r + dr, c + dc)
                if neighbor in fresh_set:
                    fresh_set.remove(neighbor)
                    queue.append(neighbor)

    return minutes_passed if not fresh_set else -1
