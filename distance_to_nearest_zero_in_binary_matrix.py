'''
Given an m x n binary matrix mat, return the distance of the nearest 0 for each cell.

The distance between two cells sharing a common edge is 1.

For example, given mat = [[0,0,0],[0,1,0],[1,1,1]], return [[0,0,0],[0,1,0],[1,2,1]].
'''

from collections import deque


def update_matrix(mat: list[list[int]]) -> list[list[int]]:
    """Calculate distance to nearest 0 for each cell using clean Multi-Source BFS."""
    if not mat or not mat[0]:
        return []

    m, n = len(mat), len(mat[0])
    dist = [[-1] * n for _ in range(m)]
    queue: deque[tuple[int, int]] = deque()

    # Enqueue all 0s as multi-source starting points
    for r in range(m):
        for c in range(n):
            if mat[r][c] == 0:
                dist[r][c] = 0
                queue.append((r, c))

    directions = ((0, 1), (1, 0), (0, -1), (-1, 0))

    while queue:
        r, c = queue.popleft()
        current_dist = dist[r][c]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                dist[nr][nc] = current_dist + 1
                queue.append((nr, nc))

    return dist


# LeetCode backward compatibility aliases
update_matrix_bfs = update_matrix
updateMatrix = update_matrix
