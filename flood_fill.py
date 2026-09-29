'''
You are given an image represented by an m x n grid of integers image, where image[i][j] represents 
the pixel value of the image. You are also given three integers sr, sc, and color. Your task is to 
perform a flood fill on the image starting from the pixel image[sr][sc].

To perform a flood fill:

Begin with the starting pixel and change its color to color.
Perform the same process for each pixel that is directly adjacent (pixels that share a side with the 
original pixel, either horizontally or vertically) and shares the same color as the starting pixel.
Keep repeating this process by checking neighboring pixels of the updated pixels and modifying their 
color if it matches the original color of the starting pixel.
The process stops when there are no more adjacent pixels of the original color to update.
Return the modified image after performing the flood fill.
'''


def flood_fill(image: list[list[int]], sr: int, sc: int, color: int) -> list[list[int]]:
    """Perform flood fill using recursive DFS."""
    original_color = image[sr][sc]
    if original_color == color:
        return image

    rows, cols = len(image), len(image[0])

    def dfs(r: int, c: int) -> None:
        image[r][c] = color
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and image[nr][nc] == original_color:
                dfs(nr, nc)

    dfs(sr, sc)
    return image


# LeetCode backward compatibility aliases
flood_fill_dfs = flood_fill
floodFill = flood_fill
