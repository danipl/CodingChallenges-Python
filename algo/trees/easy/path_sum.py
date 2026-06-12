import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (EASY - PATH SUM)  
-------------------------------------------------  
1. Target Reduction: Instead of keeping a 'running_total', subtract the 
   current node's value from the 'targetSum' as you go down.
2. Leaf Definition: A leaf is a node with 'not node.left and not node.right'. 
   This is a crucial check for path problems.
3. Boolean OR: Using 'return left_result or right_result' allows you to 
   stop searching as soon as one valid path is found.
4. Base Case Nuance: 'if not root: return False' is the standard guard, 
   but remember that a None root cannot have a sum, even if targetSum is 0.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def has_path_sum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        """
        PROBLEM: PATH SUM
        Given the root of a binary tree and an integer targetSum, return
        True if the tree has a root-to-leaf path such that adding up all
        the values along the path equals targetSum.

        REQUIREMENTS:
        - A leaf is a node with no children.
        - The path MUST end at a leaf.
        - Time Complexity: O(N).
        - Space Complexity: O(H).

        :param root: Root of the binary tree.
        :param targetSum: The value we are looking for.
        :return: Boolean.
        """
        if root is None:
            return False

        if root.left is None and root.right is None and targetSum == root.val:
            return True

        l_res = self.has_path_sum(root.left, targetSum - root.val)
        r_res = self.has_path_sum(root.right, targetSum - root.val)

        # Overall: O(N) time - visits each node exactly once across both trees
        # Overall: O(H) space - maximum recursion depth equals tree height
        return l_res or r_res


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_valid_path(self):
        # Tree: [5,4,8,11,None,13,4,7,2,None,None,None,1], Target: 22
        # Path: 5 -> 4 -> 11 -> 2 = 22
        root = TreeNode(5,
                        TreeNode(4, TreeNode(11, TreeNode(7), TreeNode(2))),
                        TreeNode(8, TreeNode(13), TreeNode(4, None, TreeNode(1))))
        self.assertTrue(self.sol.has_path_sum(root, 22))

    def test_no_valid_path(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        self.assertFalse(self.sol.has_path_sum(root, 5))

    def test_empty_tree(self):
        self.assertFalse(self.sol.has_path_sum(None, 0))

    def test_negative_values(self):
        # Target can be negative, values can be negative
        root = TreeNode(-2, None, TreeNode(-3))
        self.assertTrue(self.sol.has_path_sum(root, -5))

    def test_root_only(self):
        root = TreeNode(1)
        self.assertTrue(self.sol.has_path_sum(root, 1))


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
