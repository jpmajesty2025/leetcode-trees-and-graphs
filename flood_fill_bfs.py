'''
You are given an image represented by an m x n grid of integers image, where image[i][j] represents 
the pixel value of the image. You are also given three integers sr, sc, and color. Your task is to 
perform a flood fill on the image starting from the pixel image[sr][sc].

This module implements Iterative BFS for stack-safe pixel filling.
'''

from collections import deque


def flood_fill_bfs(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    """Perform flood fill using iterative BFS."""
    original_color = image[sr][sc]
    if original_color == color:
        return image

    rows, cols = len(image), len(image[0])
    image[sr][sc] = color
    queue = deque([(sr, sc)])

    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == original_color:
                image[nr][nc] = color
                queue.append((nr, nc))

    return image


# Aliases
flood_fill = flood_fill_bfs
floodFill = flood_fill_bfs
