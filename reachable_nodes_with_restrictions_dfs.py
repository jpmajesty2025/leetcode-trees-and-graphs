'''
There is an undirected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.

You are given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that 
there is an edge between nodes ai and bi in the tree. You are also given an integer array restricted 
which represents restricted nodes.

Return the maximum number of nodes you can reach from node 0 without visiting a restricted node.

Note that node 0 will not be a restricted node.
'''


def reachable_nodes_dfs(n: int, edges: list[list[int]], restricted: list[int]) -> int:
    """Find the maximum number of nodes reachable from node 0 using iterative DFS with a unified visited array."""
    if n <= 0:
        return 0

    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    for node in restricted:
        visited[node] = True

    if visited[0]:
        return 0

    visited[0] = True
    stack = [0]
    count = 0

    while stack:
        curr = stack.pop()
        count += 1
        for neighbor in graph[curr]:
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)

    return count


# Aliases
reachable_nodes = reachable_nodes_dfs
reachableNodes = reachable_nodes_dfs
