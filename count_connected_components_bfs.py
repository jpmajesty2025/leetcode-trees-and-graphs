'''
You have a graph of n nodes. You are given an integer n and an array edges where edges[i] = [ai, bi] 
indicates that there is an edge between ai and bi in the graph.

Return the number of connected components in the graph.
'''

from collections import deque


def count_components_bfs(n: int, edges: list[list[int]]) -> int:
    """Count the number of connected components in an undirected graph using iterative BFS."""
    if n <= 0:
        return 0

    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    components = 0

    for i in range(n):
        if not visited[i]:
            components += 1
            visited[i] = True
            queue = deque([i])

            while queue:
                curr = queue.popleft()
                for neighbor in graph[curr]:
                    if not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

    return components


# Aliases
count_components = count_components_bfs
countComponents = count_components_bfs
