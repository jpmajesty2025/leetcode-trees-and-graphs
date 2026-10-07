'''
A company has n employees with a unique ID for each employee from 0 to n - 1. The head of the company 
is the one with headID.

Each employee has one direct manager given in the manager array where manager[i] is the direct manager 
of the i-th employee, manager[headID] = -1. Also, it is guaranteed that the subordination relationships 
have a tree structure.

The head of the company wants to inform all the company employees of an urgent piece of news. He will 
inform his direct subordinates, and they will inform their subordinates, and so on until all employees 
know about the urgent news.

The i-th employee needs informTime[i] minutes to inform all of his direct subordinates 
(i.e., After informTime[i] minutes, all his direct subordinates can start spreading the news).

Return the number of minutes needed to inform all the employees about the urgent news.

Example 1:
Input: n = 1, headID = 0, manager = [-1], informTime = [0]
Output: 0
Explanation: The head of the company is the only employee so total time is 0.

Example 2:
Input: n = 6, headID = 2, manager = [2,2,-1,2,2,2], informTime = [0,0,1,0,0,0]
Output: 1
Explanation: The head of the company with id = 2 is the direct manager of all the employees in the company and needs 1 minute to inform them all.

Constraints:
- 1 <= n <= 10^5
- 0 <= headID < n
- manager.length == n
- 0 <= manager[i] < n
- manager[headID] == -1
- informTime.length == n
- 0 <= informTime[i] <= 1000
- informTime[i] == 0 if employee i has no subordinates.
- It is guaranteed that all the employees can be informed.
'''

from collections import deque
from typing import List


def num_of_minutes(n: int, headID: int, manager: List[int], informTime: List[int]) -> int:
    """Calculate the maximum time to inform all employees using iterative BFS traversal.

    Time Complexity: O(N) where N is the number of employees.
    Space Complexity: O(N) for the adjacency list and BFS queue.
    """
    if n <= 1:
        return 0

    # Build adjacency list: manager -> subordinates
    adj = [[] for _ in range(n)]
    for emp_id in range(n):
        mgr = manager[emp_id]
        if mgr != -1:
            adj[mgr].append(emp_id)

    max_time = 0
    # Queue stores tuples of (employee_id, accumulated_time_reached)
    queue = deque([(headID, 0)])

    while queue:
        emp_id, time_reached = queue.popleft()
        if time_reached > max_time:
            max_time = time_reached

        time_for_subs = time_reached + informTime[emp_id]
        for sub in adj[emp_id]:
            queue.append((sub, time_for_subs))

    return max_time
