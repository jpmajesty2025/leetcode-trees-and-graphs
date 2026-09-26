'''
There are n cities. A province is a group of directly or indirectly connected cities and no other 
cities outside of the group. You are given an n x n matrix isConnected where 
isConnected[i][j] = isConnected[j][i] = 1 if the ith city and the jth city are directly connected, 
and isConnected[i][j] = 0 otherwise. Return the total number of provinces.
'''

from collections import deque


def number_of_provinces_bfs(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    visited = [False] * n
    ans = 0

    for i in range(n):
        if not visited[i]:
            ans += 1
            visited[i] = True
            queue = deque([i])
            while queue:
                curr = queue.popleft()
                for neighbor in range(n):
                    if isConnected[curr][neighbor] == 1 and not visited[neighbor]:
                        visited[neighbor] = True
                        queue.append(neighbor)

    return ans


# LeetCode backward compatibility alias
findCircleNum = number_of_provinces_bfs
