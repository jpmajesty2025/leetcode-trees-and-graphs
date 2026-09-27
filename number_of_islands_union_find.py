'''
This module contains a 2D Disjoint Set Union (Union-Find) implementation
with Path Compression and Union by Rank to count the number of islands in a 2D grid.
'''


class UnionFind2D:
    def __init__(self, grid: list[list[str]]):
        rows, cols = len(grid), len(grid[0])
        self.parent = [-1] * (rows * cols)
        self.rank = [0] * (rows * cols)
        self.count = 0

        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == '1':
                    idx = r * cols + c
                    self.parent[idx] = idx
                    self.count += 1

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1

        self.count -= 1
        return True


def number_of_islands_union_find(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    uf = UnionFind2D(grid)

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                curr = r * cols + c
                if r + 1 < rows and grid[r + 1][c] == '1':
                    uf.union(curr, (r + 1) * cols + c)
                if c + 1 < cols and grid[r][c + 1] == '1':
                    uf.union(curr, r * cols + (c + 1))

    return uf.count


# LeetCode backward compatibility alias
numIslands = number_of_islands_union_find
