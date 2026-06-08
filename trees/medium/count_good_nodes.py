import unittest
from typing import Optional

"""
PYTHON INTERVIEW CHEAT-SHEET: TREES (MEDIUM - COUNT GOOD NODES)
------------------------------------------
1. Path Maximum Tracking: Pass the running maximum down the recursion stack
   rather than recomputing it at each node. This keeps time complexity at $O(n)$.
2. Default Parameter Trick: Use `max_val=float('-inf')` as a default argument
   to handle the root's "no ancestor" edge case cleanly.
3. Pre-order DFS: Since a node's "goodness" depends on its ancestors (top-down),
   pre-order traversal (process node, then recurse) is the natural fit.
4. Walrus Operator `:=`: Python 3.8+ allows `if (new_max := max(max_val, node.val))`
   for compact inline max tracking — great for whiteboard brevity.
5. Iterative Alternative: Use a stack of `(node, current_max)` tuples to avoid
   recursion depth issues on skewed trees.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def good_nodes(self, root: Optional[TreeNode]) -> int:
        """
        PROBLEM: COUNT GOOD NODES IN A BINARY TREE

        Given the root of a binary tree, return the number of "good" nodes.

        A node X is considered "good" if there are no nodes with a value
        greater than X.val on the path from the root to X (inclusive of X's
        ancestors). The root is always a good node since it has no ancestors.

        REQUIREMENTS:
        - Return the count of good nodes.
        - A node is "good" if its value >= all values on the path from root to it.
        - Handle negative values correctly (use float('-inf') as initial max).
        - Time Complexity must be $O(n)$ where n is the number of nodes.
        - Space Complexity must be $O(h)$ where h is the tree height (recursion stack).

        :param root: Root of the binary tree.
        :return: Number of good nodes in the tree.
        """
        pass


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def _build_tree(self, values: list) -> Optional[TreeNode]:
        """Helper to build a tree from a level-order list (None for missing nodes)."""
        if not values:
            return None
        nodes = [None if v is None else TreeNode(v) for v in values]
        kids = nodes[::-1]
        root = kids.pop()
        for node in nodes:
            if node:
                if kids:
                    node.left = kids.pop()
                if kids:
                    node.right = kids.pop()
        return root

    def test_case_1(self):
        # Tree:
        #       3
        #      / \
        #     1   4
        #    /   / \
        #   3   1   5
        # Good nodes: 3(root), 4, 3(left of 1), 5 → 4 good nodes
        root = self._build_tree([3, 1, 4, 3, None, 1, 5])
        self.assertEqual(self.sol.good_nodes(root), 4)

    def test_case_2(self):
        # Tree:
        #       3
        #      /
        #     3
        #    / \
        #   4   2
        # Good nodes: 3(root), 3(left), 4 → 3 good nodes
        root = self._build_tree([3, 3, None, 4, 2])
        self.assertEqual(self.sol.good_nodes(root), 3)

    def test_case_3(self):
        # Single node tree — root is always good
        root = TreeNode(1)
        self.assertEqual(self.sol.good_nodes(root), 1)

    def test_case_4(self):
        # All decreasing values — only root is good
        # Tree: 5 -> 4 -> 3 -> 2 -> 1 (left-skewed)
        root = self._build_tree([5, 4, None, 3, None, 2, None, 1])
        self.assertEqual(self.sol.good_nodes(root), 1)

    def test_case_5(self):
        # All same values — every node is good (equal to max on path)
        root = self._build_tree([2, 2, 2, 2, 2, 2, 2])
        self.assertEqual(self.sol.good_nodes(root), 7)

    def test_case_6(self):
        # Negative values — root with negative, children with larger negatives
        # Tree:
        #      -3
        #     /  \
        #   -5   -2
        # Good nodes: -3(root), -2 → 2 good nodes
        root = self._build_tree([-3, -5, -2])
        self.assertEqual(self.sol.good_nodes(root), 2)

    def test_case_7(self):
        # Empty tree
        self.assertEqual(self.sol.good_nodes(None), 0)


if __name__ == "__main__":
    unittest.main()
