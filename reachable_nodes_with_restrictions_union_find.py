'''
There is an undirected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.

You are given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that 
there is an edge between nodes ai and bi in the tree. You are also given an integer array restricted 
which represents restricted nodes.

Return the maximum number of nodes you can reach from node 0 without visiting a restricted node.

Note that node 0 will not be a restricted node.
'''


class UnionFind:
    def __init__(self, size: int):
        self.parent = list(range(size))
        self.size = [1] * size

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> None:
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return

        # Union by size
        if self.size[root_x] < self.size[root_y]:
            self.parent[root_x] = root_y
            self.size[root_y] += self.size[root_x]
        else:
            self.parent[root_y] = root_x
            self.size[root_x] += self.size[root_y]

    def get_size(self, x: int) -> int:
        return self.size[self.find(x)]


def reachable_nodes_union_find(n: int, edges: list[list[int]], restricted: list[int]) -> int:
    """Find reachable nodes from node 0 using Union-Find without building an adjacency graph."""
    if n <= 0:
        return 0

    restricted_set = set(restricted)
    if 0 in restricted_set:
        return 0

    uf = UnionFind(n)
    for u, v in edges:
        if u not in restricted_set and v not in restricted_set:
            uf.union(u, v)

    return uf.get_size(0)


# Aliases
reachable_nodes = reachable_nodes_union_find
reachableNodes = reachable_nodes_union_find
