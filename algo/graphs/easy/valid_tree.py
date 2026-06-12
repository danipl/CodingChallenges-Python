import collections
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (EASY - VALID TREE CHECK)
------------------------------------------
1. `collections.defaultdict(list)`: Build adjacency lists without checking if key exists first.
2. Tree = Connected + Acyclic: A valid tree with n nodes must have exactly n-1 edges AND
   all nodes must be reachable from any starting node. Check both conditions.
3. Edge count shortcut: If len(edges) != n - 1, it's NOT a tree — fail immediately.
   This catches both cycles (too many edges) and disconnected graphs (too few edges).
4. BFS/DFS for connectivity: After verifying edge count, run one BFS/DFS from node 0.
   If visited count == n, the graph is connected → valid tree.
5. Union-Find alternative: Track connected components with union-find. A valid tree
   merges all nodes into exactly one component with no redundant edges.
"""


class Solution:
    def validTree(self, n: int, edges: list[list[int]]) -> bool:
        """
        PROBLEM: Valid Tree

        Given n nodes labeled from 0 to n - 1 and a list of undirected edges,
        determine if these edges form a valid tree.

        A valid tree must satisfy TWO conditions:
        1. All nodes are connected (exactly one connected component).
        2. There are no cycles in the graph.

        REQUIREMENTS:
        - Return True if the edges form a valid tree, False otherwise.
        - The graph is undirected: edge [u, v] means u ↔ v.
        - A tree with n nodes must have exactly n - 1 edges.
        - Node 0 must be able to reach all other nodes.
        - Time Complexity must be O(V + E) where V = n, E = len(edges).
        - Space Complexity must be O(V + E) for adjacency list + visited set.

        :param n: Number of nodes labeled 0 to n - 1.
        :param edges: List of undirected edges, each edge is [u, v].
        :return: True if the graph is a valid tree, False otherwise.

        Example 1:
            Input: n = 5, edges = [[0, 1], [0, 2], [0, 3], [1, 4]]
            Output: True
            Explanation: All nodes connected, no cycles — valid tree.
                    0
                   /|\
                  1 2 3
                  |
                  4

        Example 2:
            Input: n = 5, edges = [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]
            Output: False
            Explanation: Cycle exists: 1-2-3-1. Not a valid tree.

        Example 3:
            Input: n = 5, edges = [[0, 1], [2, 3]]
            Output: False
            Explanation: Disconnected — nodes {0,1} and {2,3} are separate components.

        Example 4:
            Input: n = 1, edges = []
            Output: True
            Explanation: Single node with no edges is a valid tree.
        """
        if n <= 1:
            return True
        if not edges or (len(edges) != n - 1):
            return False

        # Space: O(V + E) - adjacency list stores each edge twice (undirected graph)
        # Time: O(E) - iterate through all edges once to build graph
        graph = collections.defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        queue = collections.deque([edges[0][0]])
        visited = {edges[0][0]}

        # Time: O(V) - each node enqueued and dequeued at most once
        # Space: O(V) - queue and visited set bounded by number of nodes
        while queue:
            curr = queue.popleft()
            # Time: O(degree(curr)) per iteration; O(E) total across all nodes - each edge examined once
            # Space: O(1) per neighbor check
            for neigh in graph[curr]:
                if neigh in visited:
                    continue
                visited.add(neigh)
                queue.append(neigh)

        # Overall Time Complexity: O(V + E) - edge count check O(1), build graph O(E), BFS visits each node and edge once O(V + E)
        # Overall Space Complexity: O(V + E) - adjacency list O(V + E), visited set O(V), queue O(V)
        return n == len(visited)


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_valid_tree_star(self):
        """Star topology: center 0 connected to all others — valid tree."""
        self.assertTrue(self.sol.validTree(5, [[0, 1], [0, 2], [0, 3], [0, 4]]))

    def test_valid_tree_chain(self):
        """Linear chain: 0-1-2-3-4 — valid tree."""
        self.assertTrue(self.sol.validTree(5, [[0, 1], [1, 2], [2, 3], [3, 4]]))

    def test_cycle_detected(self):
        """Graph contains a cycle: 0-1-2-0 — not a valid tree."""
        self.assertFalse(self.sol.validTree(3, [[0, 1], [1, 2], [2, 0]]))

    def test_disconnected_components(self):
        """Two separate components: {0,1} and {2,3,4} — not a valid tree."""
        self.assertFalse(self.sol.validTree(5, [[0, 1], [2, 3], [3, 4]]))

    def test_single_node(self):
        """Single node with no edges — valid tree."""
        self.assertTrue(self.sol.validTree(1, []))

    def test_too_many_edges(self):
        """Extra edge creates cycle — not a valid tree."""
        self.assertFalse(self.sol.validTree(4, [[0, 1], [1, 2], [2, 3], [0, 3]]))

    def test_too_few_edges(self):
        """Missing edge leaves node isolated — not a valid tree."""
        self.assertFalse(self.sol.validTree(4, [[0, 1], [2, 3]]))

    def test_duplicate_edges(self):
        """Duplicate edge creates implicit cycle — not a valid tree."""
        self.assertFalse(self.sol.validTree(3, [[0, 1], [1, 2], [0, 1]]))

    def test_valid_tree_complex(self):
        """Complex but valid tree structure."""
        edges = [[0, 1], [0, 2], [1, 3], [1, 4], [2, 5], [5, 6]]
        self.assertTrue(self.sol.validTree(7, edges))

    def test_empty_graph_multiple_nodes(self):
        """Multiple nodes, no edges — each is isolated, not a tree."""
        self.assertFalse(self.sol.validTree(3, []))


if __name__ == "__main__":
    unittest.main()
