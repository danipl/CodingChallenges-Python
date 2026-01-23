import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (EASY)  
------------------------------------------  
1. Mirror Logic: When comparing symmetric trees, the left child of the 'left' 
   node must be compared to the right child of the 'right' node.
2. Helper Functions: It is common in Tree problems to define a private 
   helper _dfs(n1, n2) inside the main function to handle multiple roots.
3. Boolean Identity: Using 'is None' is more explicit and often safer 
   in interviews than 'if not node', though both work for TreeNodes.
4. Level-Order Traversal: Symmetry can also be checked level-by-level using 
   a deque, ensuring each level is a palindrome.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def is_symmetric(self, root: Optional[TreeNode]) -> bool:
        """
        PROBLEM: SYMMETRIC TREE
        Given the root of a binary tree, check whether it is a mirror of
        itself (i.e., symmetric around its center).

        REQUIREMENTS:
        - Return True if the tree is symmetric, False otherwise.
        - An empty tree is considered symmetric.
        - Time Complexity must be O(N).
        - Space Complexity must be O(H).

        :param root: Root of the binary tree.
        :return: Boolean indicating if the tree is a mirror.
        """
        if root is None:
            return True

        def compare(s1: Optional[TreeNode], s2: Optional[TreeNode]) -> bool:
            if s1 is None and s2 is None:
                return True
            if s1 is None or s2 is None:
                return False

            eq = s1.val == s2.val
            # O(N) time: visits all left nodes | O(H) space: recursive call stack depth
            outer = compare(s1.left, s2.right)
            # O(N) time: visits all right nodes | O(H) space: recursive call stack depth
            inner = compare(s1.right, s2.left)

            # Overall: O(N) time - visits each node exactly once across both trees
            # Overall: O(H) space - maximum recursion depth equals tree height
            return eq and outer and inner

        return compare(root.left, root.right)


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_symmetric(self):
        # Tree: [1,2,2,3,4,4,3]
        root = TreeNode(1,
                        TreeNode(2, TreeNode(3), TreeNode(4)),
                        TreeNode(2, TreeNode(4), TreeNode(3)))
        self.assertTrue(self.sol.is_symmetric(root))

    def test_asymmetric(self):
        # Tree: [1,2,2,None,3,None,3]
        root = TreeNode(1,
                        TreeNode(2, None, TreeNode(3)),
                        TreeNode(2, None, TreeNode(3)))
        self.assertFalse(self.sol.is_symmetric(root))

    def test_single_node(self):
        root = TreeNode(1)
        self.assertTrue(self.sol.is_symmetric(root))

    def test_empty_tree(self):
        self.assertTrue(self.sol.is_symmetric(None))

    def test_mismatched_values(self):
        # Tree: [1,2,3]
        root = TreeNode(1, TreeNode(2), TreeNode(3))
        self.assertFalse(self.sol.is_symmetric(root))


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
