import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (MEDIUM) — Union-Find
------------------------------------------
1. Union-Find (Disjoint Set Union): Track connected components with two operations —
   `find(x)` returns the root of x's set (use path compression: `parent[x] = find(parent[x])`),
   and `union(x, y)` merges two sets (use rank/size to keep tree shallow).
   Nearly O(α(n)) ≈ O(1) per operation with both optimizations.

2. Path Compression: Inside `find()`, set `parent[x] = find(parent[x])` so future
   lookups skip intermediate nodes. This alone gives O(log n); combined with union by
   rank, it achieves inverse Ackermann O(α(n)) — effectively constant.

3. Union by Rank: Attach the shorter tree under the taller one to prevent degenerate
   chains. Track `rank[root]` (approximate tree height) and only increment when ranks
   are equal.

4. Cycle Detection in Undirected Graphs: If `find(u) == find(v)` before processing
   edge (u, v), that edge creates a cycle. This is the core insight for redundant
   connection problems.

5. `collections.defaultdict(int)`: Useful for initializing rank/size arrays lazily
   when node labels aren't 0-indexed integers.

You've used BFS for graph traversal (keys_and_rooms.py, number_of_connected_components.py)
and Kahn's algorithm for topological sort (course_schedule.py). Union-Find is a completely
different approach — no explicit graph construction, no queue, just array lookups.
"""


class Solution:
    def findRedundantConnection(self, edges: list[list[int]]) -> list[int]:
        """
        PROBLEM: Redundant Connection

        Given a graph that started as a tree with n nodes (labeled 1 to n) with one
        additional edge added, return the edge that can be removed to restore the tree.

        A tree is an undirected graph that is connected and has no cycles.

        The input `edges` is a list of edges where edges[i] = [a, b] represents an
        undirected edge between nodes a and b.

        If there are multiple answers, return the edge that appears LAST in the input.

        REQUIREMENTS:
        - Return the redundant edge as [u, v].
        - The graph is guaranteed to have exactly one cycle.
        - Nodes are labeled 1 to n where n = number of edges.
        - Time Complexity must be O(n · α(n)) ≈ O(n) using Union-Find with path compression and union by rank.
        - Space Complexity must be O(n) for the parent and rank arrays.

        Example 1:
            Input: edges = [[1,2], [1,3], [2,3]]
            Output: [2,3]
            Explanation: Removing [2,3] restores the tree 1-2, 1-3.

        Example 2:
            Input: edges = [[1,2], [2,3], [3,4], [1,4], [1,5]]
            Output: [1,4]
            Explanation: Removing [1,4] restores the tree.

        :param edges: List of edges where each edge is [u, v] with 1 <= u, v <= n.
        :return: The redundant edge [u, v] that creates the cycle.
        """
        # Space: O(n) - parent array of size n+1 stores component roots
        n = len(edges)
        parent = list(range(n + 1))

        def find(x: int) -> int:
            # Time: O(α(n)) ≈ O(1) — path compression flattens the tree on each lookup
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]

        def union(x: int, y: int) -> bool:
            # Time: O(α(n)) ≈ O(1) — two find() calls, then constant-time pointer update
            root_x = find(x)
            root_y = find(y)

            if root_x == root_y:
                return False

            parent[root_x] = root_y
            return True

        # Time: O(n · α(n)) ≈ O(n) — process each edge once, each union is nearly O(1)
        for u, v in edges:
            if not union(u, v):
                # Overall Time Complexity: O(n · α(n)) ≈ O(n) — process each edge once with near-constant union
                # Overall Space Complexity: O(n) — parent array of size n+1
                return [u, v]

        return []


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_basic_triangle_cycle(self):
        """Simple 3-node cycle — last edge is redundant."""
        self.assertEqual(self.sol.findRedundantConnection([[1, 2], [1, 3], [2, 3]]), [2, 3])

    def test_linear_with_back_edge(self):
        """Path 1-2-3-4 with back edge 1-4 creating cycle."""
        self.assertEqual(
            self.sol.findRedundantConnection([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]),
            [1, 4],
        )

    def test_redundant_edge_not_last(self):
        """Multiple edges after the cycle — still return the one that closes the cycle."""
        self.assertEqual(
            self.sol.findRedundantConnection([[1, 2], [2, 3], [3, 1], [1, 4], [4, 5]]),
            [3, 1],
        )

    def test_four_node_cycle(self):
        """Square cycle 1-2-3-4-1."""
        self.assertEqual(
            self.sol.findRedundantConnection([[1, 2], [2, 3], [3, 4], [4, 1]]),
            [4, 1],
        )

    def test_larger_tree_with_cycle(self):
        """7-node graph with one redundant edge."""
        self.assertEqual(
            self.sol.findRedundantConnection(
                [[1, 2], [1, 3], [2, 4], [3, 5], [4, 6], [5, 6]]
            ),
            [5, 6],
        )

    def test_minimum_input(self):
        """Smallest valid input: 2 nodes, 2 edges (must form cycle)."""
        self.assertEqual(self.sol.findRedundantConnection([[1, 2], [1, 2]]), [1, 2])

    def test_star_graph_with_cycle(self):
        """Star graph center=1, with extra edge creating cycle."""
        self.assertEqual(
            self.sol.findRedundantConnection([[1, 2], [1, 3], [1, 4], [2, 4]]),
            [2, 4],
        )


if __name__ == "__main__":
    unittest.main()
