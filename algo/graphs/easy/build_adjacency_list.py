import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (EASY - ADJACENCY LIST CONSTRUCTION)
------------------------------------------
1. `collections.defaultdict(list)`: Build adjacency lists without checking if key exists first.
   `graph[u].append(v)` works even if `u` hasn't been seen — auto-creates empty list.
2. Undirected vs directed: Undirected edges require `graph[u].append(v)` AND `graph[v].append(u)`.
   Directed edges only need one direction. Forgetting this is the #1 interview bug.
3. Edge list to adjacency list: Iterate once over edges — O(E) time, O(V + E) space.
   This is the universal first step for almost every graph problem.
4. Ensure all nodes exist: Some nodes may have no edges (isolated). Use `range(n)` or a set
   of all node labels to guarantee they appear in the adjacency list.
5. `dict.get(key, [])` vs `defaultdict`: `defaultdict` is cleaner but `get` is safer when
   you need to distinguish "key exists with empty list" from "key doesn't exist".
"""


class Solution:
    def buildAdjacencyList(self, n: int, edges: list[list[int]], directed: bool = False) -> dict[int, list[int]]:
        """
        PROBLEM: Build Adjacency List from Edge List

        Given n nodes labeled from 0 to n - 1 and a list of edges,
        construct and return an adjacency list representation of the graph.

        An adjacency list is a dictionary where each key is a node label,
        and its value is a list of neighboring node labels.

        REQUIREMENTS:
        - Return a dict[int, list[int]] representing the adjacency list.
        - If directed=False (default), edges are undirected: [u, v] means u→v AND v→u.
        - If directed=True, edges are directed: [u, v] means only u→v.
        - ALL nodes from 0 to n - 1 must appear as keys, even if they have no edges.
        - Neighbor lists should be sorted in ascending order for deterministic output.
        - Time Complexity must be O(V + E) where V = n, E = len(edges).
        - Space Complexity must be O(V + E) for the adjacency list.

        :param n: Number of nodes labeled 0 to n - 1.
        :param edges: List of edges, each edge is [u, v].
        :param directed: If True, edges are directed; if False (default), undirected.
        :return: Adjacency list as dict[int, list[int]].

        Example 1:
            Input: n = 4, edges = [[0, 1], [1, 2], [2, 3]], directed = False
            Output: {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]}
            Explanation: Undirected — each edge creates connections in both directions.

        Example 2:
            Input: n = 4, edges = [[0, 1], [1, 2], [2, 3]], directed = True
            Output: {0: [1], 1: [2], 2: [3], 3: []}
            Explanation: Directed — edges go only one way.

        Example 3:
            Input: n = 5, edges = [], directed = False
            Output: {0: [], 1: [], 2: [], 3: [], 4: []}
            Explanation: No edges — all nodes are isolated but still present as keys.
        """
        # Space: O(V) - pre-allocate V empty lists, one per node
        # Time: O(V) - iterate range(n) once
        graph = {i: [] for i in range(n)}

        # Time: O(E) - each edge processed once (2 appends if undirected, still O(E))
        # Space: O(E) - each edge stored once (directed) or twice (undirected) in neighbor lists
        for u, v in edges:
            graph[u].append(v)
            if not directed:
                graph[v].append(u)

        # Time: O(Σ dᵢ log dᵢ) ≤ O(E log E) - sort each node's neighbor list, bounded by total edges
        # Space: O(log E) - Timsort auxiliary space per sort call
        for l in graph.values():
            l.sort()

        # Overall Time Complexity: O(V + E log E) - dict init O(V), edge processing O(E), sorting O(E log E)
        # Overall Space Complexity: O(V + E) - dict keys O(V), neighbor lists O(E)
        return graph


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_undirected_chain(self):
        """Linear chain with undirected edges."""
        result = self.sol.buildAdjacencyList(4, [[0, 1], [1, 2], [2, 3]], directed=False)
        self.assertEqual(result, {0: [1], 1: [0, 2], 2: [1, 3], 3: [2]})

    def test_directed_chain(self):
        """Linear chain with directed edges."""
        result = self.sol.buildAdjacencyList(4, [[0, 1], [1, 2], [2, 3]], directed=True)
        self.assertEqual(result, {0: [1], 1: [2], 2: [3], 3: []})

    def test_no_edges(self):
        """No edges — all nodes isolated but present."""
        result = self.sol.buildAdjacencyList(5, [], directed=False)
        self.assertEqual(result, {0: [], 1: [], 2: [], 3: [], 4: []})

    def test_single_node(self):
        """Only one node — trivial adjacency list."""
        result = self.sol.buildAdjacencyList(1, [], directed=False)
        self.assertEqual(result, {0: []})

    def test_undirected_star(self):
        """Star topology: center node 0 connected to all others."""
        result = self.sol.buildAdjacencyList(4, [[0, 1], [0, 2], [0, 3]], directed=False)
        self.assertEqual(result, {0: [1, 2, 3], 1: [0], 2: [0], 3: [0]})

    def test_directed_cycle(self):
        """Directed cycle: 0→1→2→0."""
        result = self.sol.buildAdjacencyList(3, [[0, 1], [1, 2], [2, 0]], directed=True)
        self.assertEqual(result, {0: [1], 1: [2], 2: [0]})

    def test_duplicate_edges_undirected(self):
        """Duplicate edges should appear multiple times in neighbor list."""
        result = self.sol.buildAdjacencyList(3, [[0, 1], [0, 1], [1, 2]], directed=False)
        self.assertEqual(result, {0: [1, 1], 1: [0, 0, 2], 2: [1]})

    def test_isolated_nodes_with_edges(self):
        """Some nodes have edges, others are isolated."""
        result = self.sol.buildAdjacencyList(6, [[0, 1], [3, 4]], directed=False)
        self.assertEqual(result, {0: [1], 1: [0], 2: [], 3: [4], 4: [3], 5: []})

    def test_self_loop_undirected(self):
        """Self-loop: node connected to itself."""
        result = self.sol.buildAdjacencyList(3, [[1, 1], [0, 2]], directed=False)
        self.assertEqual(result, {0: [2], 1: [1, 1], 2: [0]})

    def test_self_loop_directed(self):
        """Self-loop in directed graph."""
        result = self.sol.buildAdjacencyList(3, [[1, 1], [0, 2]], directed=True)
        self.assertEqual(result, {0: [2], 1: [1], 2: []})


if __name__ == "__main__":
    unittest.main()
