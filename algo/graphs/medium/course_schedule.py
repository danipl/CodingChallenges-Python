import collections
import unittest
from typing import List

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (MEDIUM - TOPOLOGICAL SORT)
------------------------------------------
1. `collections.defaultdict(list)`: Build adjacency lists without checking if key exists first.
2. In-degree array: `in_degree = [0] * n` — track how many prerequisites each node has.
   Nodes with in_degree 0 are "ready to process" — no dependencies blocking them.
3. Kahn's Algorithm (BFS topological sort): 
   - Start with all in_degree-0 nodes in a queue.
   - Process each: decrement neighbors' in_degree; if any hits 0, enqueue it.
   - If you process all n nodes → no cycle → valid topological ordering exists.
   - If some nodes remain unprocessed → cycle detected → impossible to order.
4. `collections.deque`: O(1) popleft() for the BFS queue. Never use `list.pop(0)` — it's O(n).
5. Cycle detection via topological sort: If `len(processed) < n` after BFS, a cycle exists.
   This is cleaner than DFS-based cycle detection for interview settings.

🆕 PATTERN TRANSFER: You've used BFS in trees (level_order_traversal.py) and graphs
(keys_and_rooms.py, number_of_connected_components.py). Topological sort is BFS + in_degree
tracking — same queue mechanics, but you only enqueue nodes when ALL dependencies are resolved.
"""


class Solution:
    def can_finish(self, num_courses: int, prerequisites: List[List[int]]) -> bool:
        """
        PROBLEM: COURSE SCHEDULE
        There are a total of num_courses courses you have to take, labeled from 0 to num_courses - 1.
        You are given an array prerequisites where prerequisites[i] = [a, b] indicates that you
        MUST take course b before you can take course a.

        For example, the pair [0, 1] indicates that to take course 0 you must first take course 1.

        Return True if you can finish all courses. Otherwise, return False.

        REQUIREMENTS:
        - Return True if all courses can be completed (no cyclic dependencies), False otherwise.
        - A cycle in prerequisites means impossible to finish (e.g., [0,1] and [1,0]).
        - num_courses >= 1.
        - prerequisites may be empty (no dependencies — always possible).
        - Time Complexity must be O(V + E) where V = num_courses, E = len(prerequisites).
        - Space Complexity must be O(V + E) for adjacency list + in_degree array + queue.

        :param num_courses: Total number of courses, labeled 0 to num_courses - 1.
        :param prerequisites: List of prerequisite pairs [course, prerequisite].
        :return: True if all courses can be finished, False if a cycle exists.

        Example 1:
            Input: num_courses = 2, prerequisites = [[1, 0]]
            Output: True
            Explanation: Take course 0 first, then course 1. No cycle.

        Example 2:
            Input: num_courses = 2, prerequisites = [[1, 0], [0, 1]]
            Output: False
            Explanation: Course 0 requires course 1, and course 1 requires course 0. Cycle!

        Example 3:
            Input: num_courses = 5, prerequisites = [[1, 0], [2, 0], [3, 1], [3, 2]]
            Output: True
            Explanation: Valid order: 0 → 1 → 3 and 0 → 2 → 3. No cycle.
        """
        if not prerequisites:
            return True

        in_degree = [0] * num_courses
        graph = collections.defaultdict(list)

        # Time: O(E) - iterate through all prerequisite pairs once
        # Space: O(V) - in_degree array stores V entries
        for course, prereq in prerequisites:
            graph[prereq].append(course)
            in_degree[course] += 1

        queue = collections.deque()

        # Time: O(V) - scan all courses to find zero in-degree nodes
        for course, degree in enumerate(in_degree):
            if degree == 0:
                queue.append(course)

        processed = 0

        # Time: O(V + E) total - each node enqueued once, each edge traversed once
        # Space: O(V) - queue holds at most V nodes
        while queue:
            current = queue.popleft()
            processed += 1
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Overall Time Complexity: O(V + E) - graph build O(E), queue init O(V), BFS O(V + E)
        # Overall Space Complexity: O(V + E) - graph stores E edges, in_degree O(V), queue O(V)
        return processed == num_courses


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_no_prerequisites(self):
        """No dependencies — trivially possible."""
        self.assertTrue(self.sol.can_finish(4, []))

    def test_simple_linear_chain(self):
        """0 → 1 → 2 → 3 — valid ordering exists."""
        self.assertTrue(self.sol.can_finish(4, [[1, 0], [2, 1], [3, 2]]))

    def test_simple_cycle(self):
        """0 requires 1, 1 requires 0 — impossible."""
        self.assertFalse(self.sol.can_finish(2, [[1, 0], [0, 1]]))

    def test_diamond_dependency(self):
        """0 → 1 → 3 and 0 → 2 → 3 — valid, no cycle."""
        self.assertTrue(self.sol.can_finish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]))

    def test_three_node_cycle(self):
        """0 → 1 → 2 → 0 — cycle of length 3."""
        self.assertFalse(self.sol.can_finish(3, [[1, 0], [2, 1], [0, 2]]))

    def test_single_course(self):
        """Only one course — always possible."""
        self.assertTrue(self.sol.can_finish(1, []))

    def test_disconnected_components(self):
        """Two separate chains — both valid."""
        self.assertTrue(self.sol.can_finish(6, [[1, 0], [3, 2], [4, 3], [5, 4]]))

    def test_cycle_in_subgraph(self):
        """Valid chain + a separate cycle — overall impossible."""
        self.assertFalse(self.sol.can_finish(5, [[1, 0], [2, 1], [3, 4], [4, 3]]))

    def test_duplicate_prerequisites(self):
        """Duplicate edges should not affect result."""
        self.assertTrue(self.sol.can_finish(2, [[1, 0], [1, 0]]))

    def test_self_loop(self):
        """Course requires itself — cycle of length 1."""
        self.assertFalse(self.sol.can_finish(2, [[1, 1]]))


if __name__ == "__main__":
    unittest.main()
