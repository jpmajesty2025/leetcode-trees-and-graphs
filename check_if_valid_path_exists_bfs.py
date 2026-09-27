'''
There is a bi-directional graph with n vertices, where each vertex is labeled from 0 to n - 1 (inclusive). 
The edges in the graph are represented as a 2D integer array edges, where each edges[i] = [ui, vi] 
denotes a bi-directional edge between vertex ui and vertex vi. Every vertex pair is connected by at 
most one edge, and no vertex has an edge to itself.

You want to determine if there is a valid path that exists from vertex source to vertex destination.

Given edges and the integers n, source, and destination, return true if there is a valid path from source 
to destination, or false otherwise.
'''

from collections import deque


def valid_path_bfs(n: int, edges: list[list[int]], source: int, destination: int) -> bool:
    """Determine if a valid path exists from source to destination using BFS."""
    if source == destination:
        return True

    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    visited = [False] * n
    visited[source] = True
    queue = deque([source])

    while queue:
        curr = queue.popleft()
        for neighbor in graph[curr]:
            if neighbor == destination:
                return True
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    return False


# Aliases
valid_path = valid_path_bfs
validPath = valid_path_bfs
