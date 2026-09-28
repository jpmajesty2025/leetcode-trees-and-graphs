'''
Given an n x n binary matrix grid, return the length of the shortest clear path in the matrix. 
If there is no clear path, return -1.

A clear path in a binary matrix is a path from the top-left cell (i.e., (0, 0)) to the bottom-right 
cell (i.e., (n - 1, n - 1)) such that:

All the visited cells of the path are 0.
All the adjacent cells of the path are 8-directionally connected (i.e., they are different and they 
share an edge or a corner).
The length of a clear path is the number of visited cells of this path.
'''

from collections import deque


def shortest_path_binary_matrix(grid: list[list[int]]) -> int:
    """Find the shortest clear path in a binary matrix using optimized 8-directional BFS."""
    if not grid or not grid[0] or grid[0][0] == 1 or grid[-1][-1] == 1:
        return -1

    n = len(grid)
    if n == 1:
        return 1

    visited = [[False] * n for _ in range(n)]
    visited[0][0] = True
    queue = deque([(0, 0, 1)])  # (row, col, steps)

    # 8-directional deltas
    directions = (
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    )

    while queue:
        r, c, steps = queue.popleft()

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 0 and not visited[nr][nc]:
                if nr == n - 1 and nc == n - 1:
                    return steps + 1
                visited[nr][nc] = True
                queue.append((nr, nc, steps + 1))

    return -1


# LeetCode backward compatibility aliases
shortest_path_binary_matrix_bfs = shortest_path_binary_matrix
shortestPathBinaryMatrix = shortest_path_binary_matrix
