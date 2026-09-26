'''
There are n cities. A province is a group of directly or indirectly connected cities and no other 
cities outside of the group. You are given an n x n matrix isConnected where 
isConnected[i][j] = isConnected[j][i] = 1 if the ith city and the jth city are directly connected, 
and isConnected[i][j] = 0 otherwise. Return the total number of provinces.
'''


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.rank = [0] * size
        self.count = size

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


def number_of_provinces_union_find(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    if n == 0:
        return 0

    uf = UnionFind(n)
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)

    return uf.count


# LeetCode backward compatibility alias
findCircleNum = number_of_provinces_union_find
