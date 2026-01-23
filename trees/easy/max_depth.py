import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (EASY - DEPTH)  
-------------------------------------------------  
1. max() function: Use max(left_height, right_height) to find the longest 
   path in a single line.
2. Bottom-up thinking: In recursion, think about what the base case (None) 
   returns (usually 0 for height) and how the parent increments that.
3. Tail Recursion: Python does NOT optimize tail recursion, so deep 
   trees will always consume stack space proportional to height.
4. Level-Order alternative: You can also solve this with BFS; the number 
   of levels processed in the queue equals the max depth.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def max_depth(self, root: Optional[TreeNode]) -> int:
        """
        PROBLEM: MAXIMUM DEPTH OF BINARY TREE
        Given the root of a binary tree, return its maximum depth.
        A binary tree's maximum depth is the number of nodes along the
        longest path from the root node down to the farthest leaf node.

        REQUIREMENTS:
        - Return the integer depth.
        - An empty tree has a depth of 0.
        - Time Complexity must be O(N).
        - Space Complexity must be O(H).

        :param root: Root of the binary tree.
        :return: Integer representing max depth.
        """
        if root is None:
            return 0

        # Overall: O(N) time - visits each node exactly once across both trees
        # Overall: O(H) space - maximum recursion depth equals tree height
        return 1 + max(self.max_depth(root.left), self.max_depth(root.right))


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_normal_tree(self):
        # Tree: [3,9,20,None,None,15,7], Depth: 3
        root = TreeNode(3,
                        TreeNode(9),
                        TreeNode(20, TreeNode(15), TreeNode(7)))
        self.assertEqual(self.sol.max_depth(root), 3)

    def test_skewed_tree(self):
        # Tree: [1,None,2,None,3], Depth: 3
        root = TreeNode(1, None, TreeNode(2, None, TreeNode(3)))
        self.assertEqual(self.sol.max_depth(root), 3)

    def test_single_node(self):
        root = TreeNode(1)
        self.assertEqual(self.sol.max_depth(root), 1)

    def test_empty_tree(self):
        self.assertEqual(self.sol.max_depth(None), 0)

    def test_two_nodes(self):
        # Tree: [1,2], Depth: 2
        root = TreeNode(1, TreeNode(2))
        self.assertEqual(self.sol.max_depth(root), 2)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
