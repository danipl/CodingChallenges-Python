import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (EASY - INVERSION)  
-------------------------------------------------  
1. Multiple Assignment: Python allows 'a, b = b, a', which is perfect for 
   swapping left and right children in a single, atomic line.
2. Return value: In many tree mutation problems, you should return the 
   root of the modified tree to allow for recursive nesting.
3. Post-order vs Pre-order: For inversion, it usually doesn't matter if 
   you swap children before or after recursing, but Pre-order (swap first) 
   is often more intuitive.
4. Iterative Swap: Just like BFS, you can use a queue/stack to visit 
   every node and swap its children manually.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def invert_tree(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        """
        PROBLEM: INVERT BINARY TREE
        Given the root of a binary tree, invert the tree (flip it
        horizontally), and return its root.

        REQUIREMENTS:
        - Every left child must become the right child, and vice versa.
        - Must handle the entire tree recursively or iteratively.
        - Time Complexity must be O(N).
        - Space Complexity must be O(H).

        :param root: Root of the binary tree.
        :return: Root of the inverted tree.
        """
        if root is None:
            return root

        root.left, root.right = root.right, root.left

        self.invert_tree(root.left)
        self.invert_tree(root.right)

        # Overall: O(N) time - visits each node exactly once across both trees
        # Overall: O(H) space - maximum recursion depth equals tree height
        return root


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_tree(self):
        # Input: [4,2,7,1,3,6,9] -> Output: [4,7,2,9,6,3,1]
        root = TreeNode(4,
                        TreeNode(2, TreeNode(1), TreeNode(3)),
                        TreeNode(7, TreeNode(6), TreeNode(9)))
        inverted = self.sol.invert_tree(root)
        self.assertEqual(inverted.val, 4)
        self.assertEqual(inverted.left.val, 7)
        self.assertEqual(inverted.right.val, 2)
        self.assertEqual(inverted.left.left.val, 9)

    def test_single_node(self):
        root = TreeNode(1)
        inverted = self.sol.invert_tree(root)
        self.assertEqual(inverted.val, 1)
        self.assertIsNone(inverted.left)

    def test_empty_tree(self):
        self.assertIsNone(self.sol.invert_tree(None))

    def test_asymmetric_tree(self):
        # Input: [1,2] -> Output: [1,None,2]
        root = TreeNode(1, TreeNode(2), None)
        inverted = self.sol.invert_tree(root)
        self.assertIsNone(inverted.left)
        self.assertEqual(inverted.right.val, 2)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
