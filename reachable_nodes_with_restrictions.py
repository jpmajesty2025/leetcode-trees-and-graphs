'''
There is an undirected tree with n nodes labeled from 0 to n - 1 and n - 1 edges.

You are given a 2D integer array edges of length n - 1 where edges[i] = [ai, bi] indicates that 
there is an edge between nodes ai and bi in the tree. You are also given an integer array restricted 
which represents restricted nodes.

Return the maximum number of nodes you can reach from node 0 without visiting a restricted node.

Note that node 0 will not be a restricted node.
'''

from collections import deque


def reachable_nodes(n: int, edges: list[list[int]], restricted: list[int]) -> int:
    """Find the maximum number of nodes reachable from node 0 using optimized BFS with a unified visited array."""
    if n <= 0:
        return 0

    # Build adjacency list using fixed-size lists
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    # Pre-mark restricted nodes directly into the visited array
    visited = [False] * n
    for node in restricted:
        visited[node] = True

    if visited[0]:
        return 0

    visited[0] = True
    queue = deque([0])
    count = 0

    while queue:
        curr = queue.popleft()
        count += 1
        for neighbor in graph[curr]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)

    return count


# LeetCode backward compatibility aliases
reachable_nodes_bfs = reachable_nodes
reachableNodes = reachable_nodes
