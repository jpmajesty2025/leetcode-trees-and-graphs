'''
You are given a positive integer n representing the number of nodes of a Directed Acyclic Graph (DAG). 
The nodes are numbered from 0 to n - 1 (inclusive).

You are also given a 2D integer array edges, where edges[i] = [fromi, toi] denotes that there is a 
unidirectional edge from fromi to toi in the graph.

Return a list answer, where answer[i] is the list of ancestors of the ith node, sorted in ascending order.

A node u is an ancestor of another node v if u can reach v via a set of edges.

Example 1:
Input: n = 8, edges = [[0,3],[0,4],[1,3],[2,4],[2,7],[3,5],[3,6],[3,7],[4,6]]
Output: [[],[],[],[0,1],[0,2],[0,1,3],[0,1,2,3,4],[0,1,2,3]]

Example 2:
Input: n = 5, edges = [[0,1],[0,2],[0,3],[0,4],[1,2],[1,3],[1,4],[2,3],[2,4],[3,4]]
Output: [[],[0],[0,1],[0,1,2],[0,1,2,3]]

Constraints:
- 1 <= n <= 1000
- 0 <= edges.length <= min(2000, n * (n - 1) / 2)
- edges[i].length == 2
- 0 <= fromi, toi <= n - 1
- fromi != toi
- There are no duplicate edges.
- The given graph is a directed acyclic graph (DAG).
'''

from typing import List


def get_ancestors(n: int, edges: List[List[int]]) -> List[List[int]]:
    """Find all ancestors of each node in a DAG using forward DFS.

    Iterating ancestor candidates u in ascending order (0 to n - 1) guarantees
    that each node v receives ancestors in naturally sorted ascending order,
    eliminating the need for post-sorting.

    Time Complexity: O(V * (V + E)) where V = n and E = len(edges).
    Space Complexity: O(V + E) for adjacency list and visited tracking.
    """
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)

    ancestors = [[] for _ in range(n)]

    def dfs(ancestor: int, current: int, visited: List[bool]) -> None:
        visited[current] = True
        for neighbor in adj[current]:
            if not visited[neighbor]:
                ancestors[neighbor].append(ancestor)
                dfs(ancestor, neighbor, visited)

    # Search outward from each ancestor candidate in ascending order
    for u in range(n):
        visited = [False] * n
        dfs(u, u, visited)

    return ancestors
