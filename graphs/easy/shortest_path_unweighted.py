import collections
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (EASY - BFS SHORTEST PATH)
------------------------------------------
1. `collections.deque`: O(1) popleft() for BFS queue. Never use `list.pop(0)` — it's O(n).
2. BFS for shortest path: In unweighted graphs, BFS guarantees shortest path because
   it explores nodes in order of distance from the source. First time you reach the
   target = minimum number of edges.
3. Distance tracking: Store `(node, distance)` tuples in the queue, OR maintain a
   separate `dist` dictionary/array. Both are O(N) space.
4. `visited` set prevents cycles: Always check `if neighbor not in visited` before
   enqueueing. Without this, cycles cause infinite loops.
5. Early exit: `if current == target: return distance` — no need to explore the
   entire graph once the target is found. This is a key optimization.
"""


class Solution:
    def shortestPath(self, n: int, edges: list[list[int]], start: int, end: int) -> int:
        """
        PROBLEM: Shortest Path in Unweighted Graph

        Given an undirected graph with n nodes labeled from 0 to n - 1,
        a list of edges, a start node, and an end node, return the length
        of the shortest path from start to end.

        The path length is the number of edges traversed. If no path exists,
        return -1.

        REQUIREMENTS:
        - Return the minimum number of edges from start to end.
        - Return -1 if end is unreachable from start.
        - The graph is undirected: edge [u, v] means u ↔ v.
        - If start == end, return 0.
        - Time Complexity must be O(V + E) where V = n, E = len(edges).
        - Space Complexity must be O(V + E) for adjacency list + visited set + queue.

        :param n: Number of nodes labeled 0 to n - 1.
        :param edges: List of undirected edges, each edge is [u, v].
        :param start: Starting node label.
        :param end: Target node label.
        :return: Shortest path length (number of edges), or -1 if unreachable.

        Example 1:
            Input: n = 5, edges = [[0, 1], [1, 2], [2, 3], [0, 4]], start = 0, end = 3
            Output: 3
            Explanation: Shortest path: 0 → 1 → 2 → 3 (3 edges).

        Example 2:
            Input: n = 5, edges = [[0, 1], [2, 3], [3, 4]], start = 0, end = 4
            Output: -1
            Explanation: Node 0 is in component {0, 1}, node 4 is in {2, 3, 4}. No path.

        Example 3:
            Input: n = 3, edges = [[0, 1], [1, 2]], start = 0, end = 0
            Output: 0
            Explanation: Start equals end — zero edges needed.
        """
        if start == end:
            return 0
        if n == 0 or not edges:
            return -1

        # Space: O(V + E) - adjacency list stores each edge twice (undirected)
        # Time: O(E) - iterate through all edges once to build graph
        graph = collections.defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        # Space: O(V) - queue stores at most V (node, dist) tuples
        queue = collections.deque([(start, 0)])
        # Space: O(V) - visited set stores at most V nodes
        visited = {start}

        # Time: O(V) - each node dequeued at most once
        # Space: O(V) - queue + visited bounded by V
        while queue:
            curr, dist = queue.popleft()
            # Time: O(degree(curr)) per iteration; O(E) total across all nodes - each edge examined once
            for neighbor in graph[curr]:
                if neighbor in visited:
                    continue
                visited.add(neighbor)
                if neighbor == end:
                    return dist + 1
                queue.append((neighbor, dist + 1))

        # Overall Time Complexity: O(V + E) - build graph O(E), BFS visits each node and edge once
        # Overall Space Complexity: O(V + E) - adjacency list O(V + E), visited O(V), queue O(V)
        return -1


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_linear_path(self):
        """Straight line graph: 0-1-2-3, shortest path 0→3 = 3."""
        self.assertEqual(self.sol.shortestPath(4, [[0, 1], [1, 2], [2, 3]], 0, 3), 3)

    def test_shorter_path_exists(self):
        """Graph with shortcut: 0-1-2-3 and 0-3, shortest path 0→3 = 1."""
        self.assertEqual(self.sol.shortestPath(4, [[0, 1], [1, 2], [2, 3], [0, 3]], 0, 3), 1)

    def test_unreachable(self):
        """Disconnected components — no path exists."""
        self.assertEqual(self.sol.shortestPath(5, [[0, 1], [2, 3], [3, 4]], 0, 4), -1)

    def test_start_equals_end(self):
        """Start and end are the same node."""
        self.assertEqual(self.sol.shortestPath(3, [[0, 1], [1, 2]], 1, 1), 0)

    def test_single_edge(self):
        """Direct connection between start and end."""
        self.assertEqual(self.sol.shortestPath(2, [[0, 1]], 0, 1), 1)

    def test_no_edges(self):
        """No edges in the graph — unreachable unless start == end."""
        self.assertEqual(self.sol.shortestPath(3, [], 0, 2), -1)
        self.assertEqual(self.sol.shortestPath(3, [], 1, 1), 0)

    def test_star_graph(self):
        """Star topology: center 0 connected to all others."""
        self.assertEqual(self.sol.shortestPath(5, [[0, 1], [0, 2], [0, 3], [0, 4]], 1, 4), 2)

    def test_cycle_shortest(self):
        """Cycle graph: shortest path avoids going the long way."""
        # 0-1-2-3-4-0 cycle, shortest 0→3 = 2 (0-4-3) not 3 (0-1-2-3)
        self.assertEqual(self.sol.shortestPath(5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0]], 0, 3), 2)

    def test_single_node(self):
        """Only one node in the graph."""
        self.assertEqual(self.sol.shortestPath(1, [], 0, 0), 0)


if __name__ == "__main__":
    unittest.main()
