import collections
import unittest
from typing import List

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (EASY - DFS TRAVERSAL)
------------------------------------------
1. `collections.defaultdict(list)`: Build adjacency lists without checking if key exists first.
2. Recursive DFS: Simple and clean for small graphs — `def dfs(node): visited.add(node); for neighbor in graph[node]: if neighbor not in visited: dfs(neighbor)`.
3. Iterative DFS with stack: `stack = [start]; while stack: node = stack.pop()` — avoids recursion depth limits.
4. `set` for visited tracking: O(1) lookup prevents revisiting nodes and infinite loops on cycles.
5. Connected components: Loop over all nodes; if unvisited, start a new DFS/BFS — each start = one component.
"""


class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        """
        PROBLEM: Number of Connected Components in an Undirected Graph

        Given n nodes labeled from 0 to n - 1 and a list of undirected edges,
        return the number of connected components in the graph.

        A connected component is a set of nodes where every node is reachable
        from every other node in that set, and no node in the set is reachable
        from any node outside the set.

        REQUIREMENTS:
        - Return the number of connected components.
        - The graph is undirected: edge [a, b] means a connects to b AND b connects to a.
        - Nodes with no edges count as individual components.
        - Time Complexity must be O(V + E) where V = n nodes, E = number of edges.
        - Space Complexity must be O(V + E) for adjacency list + visited set.

        :param n: Number of nodes labeled 0 to n - 1.
        :param edges: List of undirected edges, each edge is [node_a, node_b].
        :return: Number of connected components in the graph.

        Example 1:
            Input: n = 5, edges = [[0, 1], [1, 2], [3, 4]]
            Output: 2
            Explanation: Component 1: {0, 1, 2}, Component 2: {3, 4}

        Example 2:
            Input: n = 5, edges = [[0, 1], [1, 2], [2, 3], [3, 4]]
            Output: 1
            Explanation: All nodes form a single chain — one component.

        Example 3:
            Input: n = 5, edges = []
            Output: 5
            Explanation: No edges — each node is its own component.
        """
        if not edges:
            return n

        # Space: O(V + E) - adjacency list stores each edge twice (undirected)
        # Time: O(E) - iterate through all edges once to build graph
        graph = collections.defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        components = 0
        visited = set()
        queue = collections.deque()

        # Time: O(V) - outer loop visits each node at most once
        for candidate in range(n):
            if candidate not in visited:
                queue.append(candidate)
                visited.add(candidate)
                components += 1
                # Time: O(V + E) total across all BFS runs - each node enqueued once, each edge examined once
                # Space: O(V) - queue and visited set store at most V nodes
                while queue:
                    current = queue.popleft()
                    for neighbor in graph[current]:
                        if neighbor not in visited:
                            queue.append(neighbor)
                            visited.add(neighbor)

        # Overall Time Complexity: O(V + E) - build graph O(E), BFS visits each node and edge once O(V + E)
        # Overall Space Complexity: O(V + E) - adjacency list O(V + E), visited set O(V), queue O(V)
        return components


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_two_components(self):
        """Graph splits into two groups."""
        self.assertEqual(self.sol.countComponents(5, [[0, 1], [1, 2], [3, 4]]), 2)

    def test_single_component_chain(self):
        """All nodes connected in a line."""
        self.assertEqual(self.sol.countComponents(5, [[0, 1], [1, 2], [2, 3], [3, 4]]), 1)

    def test_no_edges(self):
        """No edges — every node is isolated."""
        self.assertEqual(self.sol.countComponents(5, []), 5)

    def test_single_node(self):
        """Only one node — trivially one component."""
        self.assertEqual(self.sol.countComponents(1, []), 1)

    def test_fully_connected(self):
        """All nodes connected to each other (star topology)."""
        self.assertEqual(self.sol.countComponents(4, [[0, 1], [0, 2], [0, 3]]), 1)

    def test_cycle(self):
        """Nodes form a cycle — still one component."""
        self.assertEqual(self.sol.countComponents(4, [[0, 1], [1, 2], [2, 3], [3, 0]]), 1)

    def test_disconnected_pairs(self):
        """Multiple isolated pairs."""
        self.assertEqual(self.sol.countComponents(6, [[0, 1], [2, 3], [4, 5]]), 3)

    def test_duplicate_edges(self):
        """Duplicate edges should not affect component count."""
        self.assertEqual(self.sol.countComponents(3, [[0, 1], [1, 0], [1, 2], [2, 1]]), 1)

    def test_self_loop(self):
        """Self-loop should not create extra components."""
        self.assertEqual(self.sol.countComponents(3, [[0, 0], [1, 2]]), 2)


if __name__ == "__main__":
    unittest.main()
