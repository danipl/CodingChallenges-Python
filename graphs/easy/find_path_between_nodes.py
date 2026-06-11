import collections
import unittest
from typing import Optional

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (EASY - BFS PATH FINDING)
------------------------------------------
1. `collections.defaultdict(list)`: Build adjacency lists without checking if key exists first.
2. BFS with path tracking: Store `(node, path)` tuples in queue where `path` is the list of nodes
   from start to current node. First time you reach target = shortest path.
3. Parent dictionary alternative: Store `parent[node] = previous_node` during BFS, then
   backtrack from target to start to reconstruct path. Uses less memory than storing full paths.
4. `visited` set prevents cycles: Always check `if neighbor not in visited` before enqueueing.
   Without this, cycles cause infinite loops.
5. Path reconstruction from parent dict:
   ```python
   path = []
   curr = target
   while curr is not None:
       path.append(curr)
       curr = parent[curr]
   return path[::-1]  # reverse to get start→target order
   ```
"""


class Solution:
    def findPath(self, n: int, edges: list[list[int]], start: int, end: int) -> list[int]:
        """
        PROBLEM: Find Path Between Two Nodes

        Given an undirected graph with n nodes labeled from 0 to n - 1,
        a list of edges, a start node, and an end node, return the path
        from start to end as a list of node labels.

        The path should contain the minimum number of edges (shortest path).
        If no path exists, return an empty list [].

        REQUIREMENTS:
        - Return the path as a list of node labels from start to end.
        - Return [] if end is unreachable from start.
        - The graph is undirected: edge [u, v] means u ↔ v.
        - If start == end, return [start].
        - If multiple shortest paths exist, return any valid one.
        - Time Complexity must be O(V + E) where V = n, E = len(edges).
        - Space Complexity must be O(V + E) for adjacency list + visited + parent dict.

        :param n: Number of nodes labeled 0 to n - 1.
        :param edges: List of undirected edges, each edge is [u, v].
        :param start: Starting node label.
        :param end: Target node label.
        :return: List of node labels representing the path from start to end, or [] if unreachable.

        Example 1:
            Input: n = 5, edges = [[0, 1], [1, 2], [2, 3], [0, 4]], start = 0, end = 3
            Output: [0, 1, 2, 3]
            Explanation: Path: 0 → 1 → 2 → 3.

        Example 2:
            Input: n = 5, edges = [[0, 1], [2, 3], [3, 4]], start = 0, end = 4
            Output: []
            Explanation: Node 0 is in component {0, 1}, node 4 is in {2, 3, 4}. No path.

        Example 3:
            Input: n = 3, edges = [[0, 1], [1, 2]], start = 0, end = 0
            Output: [0]
            Explanation: Start equals end — path is just the start node.
        """
        if start == end:
            return [start]

        # Space: O(V + E) - adjacency list stores each edge twice (undirected)
        # Time: O(E) - iterate through all edges once to build graph
        graph = collections.defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        # Space: O(V) - parent dict stores at most V entries
        parent: dict[int, Optional[int]] = {start: None}
        # Space: O(V) - queue stores at most V nodes
        queue = collections.deque([start])
        found = False

        # Time: O(V) - each node dequeued at most once
        # Space: O(V) - queue + parent dict bounded by V
        while queue:
            curr = queue.popleft()
            neighs = graph[curr]
            # Time: O(degree(curr)) per iteration; O(E) total across all nodes - each edge examined once
            for neigh in neighs:
                if neigh in parent:
                    continue
                parent[neigh] = curr
                if neigh == end:
                    found = True
                    queue.clear()
                    break
                queue.append(neigh)

        if not found:
            return []

        # Time: O(V) - backtrack from end to start, at most V steps
        # Space: O(V) - path list stores at most V nodes
        path = []
        curr = end
        while curr is not None:
            path.append(curr)
            curr = parent[curr]

        # Overall Time Complexity: O(V + E) - build graph O(E), BFS O(V + E), backtrack O(V)
        # Overall Space Complexity: O(V + E) - adjacency list O(V + E), parent dict O(V), queue O(V)
        return path[::-1]


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_linear_path(self):
        """Straight line graph: 0-1-2-3, path 0→3."""
        result = self.sol.findPath(4, [[0, 1], [1, 2], [2, 3]], 0, 3)
        self.assertEqual(result, [0, 1, 2, 3])

    def test_shorter_path_exists(self):
        """Graph with shortcut: 0-1-2-3 and 0-3, shortest path 0→3."""
        result = self.sol.findPath(4, [[0, 1], [1, 2], [2, 3], [0, 3]], 0, 3)
        self.assertEqual(result, [0, 3])

    def test_unreachable(self):
        """Disconnected components — no path exists."""
        result = self.sol.findPath(5, [[0, 1], [2, 3], [3, 4]], 0, 4)
        self.assertEqual(result, [])

    def test_start_equals_end(self):
        """Start and end are the same node."""
        result = self.sol.findPath(3, [[0, 1], [1, 2]], 1, 1)
        self.assertEqual(result, [1])

    def test_single_edge(self):
        """Direct connection between start and end."""
        result = self.sol.findPath(2, [[0, 1]], 0, 1)
        self.assertEqual(result, [0, 1])

    def test_no_edges(self):
        """No edges in the graph — unreachable unless start == end."""
        self.assertEqual(self.sol.findPath(3, [], 0, 2), [])
        self.assertEqual(self.sol.findPath(3, [], 1, 1), [1])

    def test_star_graph_path(self):
        """Star topology: path from leaf to leaf through center."""
        result = self.sol.findPath(5, [[0, 1], [0, 2], [0, 3], [0, 4]], 1, 4)
        self.assertEqual(result, [1, 0, 4])

    def test_cycle_path(self):
        """Cycle graph: shortest path avoids going the long way."""
        result = self.sol.findPath(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], 0, 3)
        self.assertEqual(result, [0, 4, 3])

    def test_single_node(self):
        """Only one node in the graph."""
        result = self.sol.findPath(1, [], 0, 0)
        self.assertEqual(result, [0])

    def test_path_validation(self):
        """Verify returned path is valid: consecutive nodes must have edges."""
        edges = [[0, 1], [1, 2], [2, 3], [0, 4], [4, 5]]
        result = self.sol.findPath(6, edges, 0, 3)
        # Check path starts and ends correctly
        self.assertEqual(result[0], 0)
        self.assertEqual(result[-1], 3)
        # Check consecutive nodes are connected
        edge_set = {tuple(sorted(e)) for e in edges}
        for i in range(len(result) - 1):
            self.assertIn(tuple(sorted([result[i], result[i + 1]])), edge_set)


if __name__ == "__main__":
    unittest.main()
