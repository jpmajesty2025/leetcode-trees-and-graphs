'''
You are given an m x n binary matrix grid. An island is a group of 1's (representing land) connected 
4-directionally (horizontal or vertical, not diagonally.) You may assume all four edges of the grid are surrounded by water.

The area of an island is the number of cells with a value 1 in the island.

Return the maximum area of an island in grid. If there is no island, return 0.
'''


class UnionFindSize2D:
    def __init__(self, grid: list[list[int]]):
        m, n = len(grid), len(grid[0])
        self.parent = [-1] * (m * n)
        self.size = [0] * (m * n)
        self.max_size = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    idx = r * n + c
                    self.parent[idx] = idx
                    self.size[idx] = 1
                    self.max_size = max(self.max_size, 1)

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return False

        # Union by size
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
            self.max_size = max(self.max_size, self.size[root_y])
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]
            self.max_size = max(self.max_size, self.size[root_x])

        return True


def max_area_of_island_union_find(grid: list[list[int]]) -> int:
    """Find the maximum area of an island using 2D Union-Find tracking component sizes."""
    if not grid or not grid[0]:
        return 0

    m, n = len(grid), len(grid[0])
    uf = UnionFindSize2D(grid)

    for r in range(m):
        for c in range(n):
            if grid[r][c] == 1:
                curr = r * n + c
                if r + 1 < m and grid[r + 1][c] == 1:
                    uf.union(curr, (r + 1) * n + c)
                if c + 1 < n and grid[r][c + 1] == 1:
                    uf.union(curr, r * n + (c + 1))

    return uf.max_size


# Aliases
max_area_of_island = max_area_of_island_union_find
maxAreaOfIsland = max_area_of_island_union_find
