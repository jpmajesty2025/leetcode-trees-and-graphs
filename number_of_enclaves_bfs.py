'''
Count the number of enclaves using multi-source Breadth-First Search (BFS).
Non-destructive: preserves the original grid.
'''

from collections import deque
from typing import List


def num_enclaves_bfs(grid: List[List[int]]) -> int:
    """Count land cells that cannot reach the grid boundary using multi-source BFS.

    Time Complexity: O(M * N) where M is rows and N is columns.
    Space Complexity: O(M * N) for the queue and visited matrix.
    """
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    queue = deque()

    # Seed multi-source BFS with all boundary land cells
    for c in range(cols):
        if grid[0][c] == 1:
            visited[0][c] = True
            queue.append((0, c))
        if grid[rows - 1][c] == 1 and not visited[rows - 1][c]:
            visited[rows - 1][c] = True
            queue.append((rows - 1, c))

    for r in range(rows):
        if grid[r][0] == 1 and not visited[r][0]:
            visited[r][0] = True
            queue.append((r, 0))
        if grid[r][cols - 1] == 1 and not visited[r][cols - 1]:
            visited[r][cols - 1] = True
            queue.append((r, cols - 1))

    # Multi-source BFS traversal
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        r, c = queue.popleft()
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1 and not visited[nr][nc]:
                visited[nr][nc] = True
                queue.append((nr, nc))

    # Count all interior land cells not visited from the boundary
    enclave_count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not visited[r][c]:
                enclave_count += 1

    return enclave_count
