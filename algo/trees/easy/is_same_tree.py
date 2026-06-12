import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (EASY)  
------------------------------------------  
1. Optional[Type]: Use from the 'typing' module to clearly denote when a node 
   can be 'None', which is essential for tree leaf terminations.
2. Recursive Depth: Python has a default recursion limit (usually 1000). For 
   extremely deep trees, sys.setrecursionlimit() might be needed, though 
   interviewers usually prefer iterative solutions if this is a concern.
3. Tuple Packing for BFS/DFS: When using stacks or queues, you can store 
   state easily: stack.append((node, current_depth)).
4. Logical Short-circuiting: Use 'if not root: return' as a guard clause 
   to handle empty trees or leaf children cleanly.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def is_same_tree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        """
        PROBLEM: SAME TREE
        Given the roots of two binary trees 'p' and 'q', write a function to
        check if they are the same or not. Two binary trees are considered
        the same if they are structurally identical, and the nodes have the
        same values.

        REQUIREMENTS:
        - Return True if the trees are equivalent, False otherwise.
        - Handle null (None) nodes gracefully.
        - Time Complexity must be O(N), where N is the number of nodes.
        - Space Complexity must be O(H), where H is the height of the tree.

        :param p: Root of the first binary tree.
        :param q: Root of the second binary tree.
        :return: Boolean indicating structural and value equality.
        """
        if not p and not q:
            return True
        if not p or not q:
            return False

        eq = p.val == q.val
        # O(N) time: visits all left nodes | O(H) space: recursive call stack depth
        l_res = self.is_same_tree(p.left, q.left)
        # O(N) time: visits all right nodes | O(H) space: recursive call stack depth
        r_res = self.is_same_tree(p.right, q.right)

        # Overall: O(N) time - visits each node exactly once across both trees
        # Overall: O(H) space - maximum recursion depth equals tree height
        return eq and l_res and r_res


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_identical_trees(self):
        # Tree 1: [1,2,3], Tree 2: [1,2,3]
        p = TreeNode(1, TreeNode(2), TreeNode(3))
        q = TreeNode(1, TreeNode(2), TreeNode(3))
        self.assertTrue(self.sol.is_same_tree(p, q))

    def test_different_values(self):
        # Tree 1: [1,2], Tree 2: [1,None,2]
        p = TreeNode(1, TreeNode(2))
        q = TreeNode(1, None, TreeNode(2))
        self.assertFalse(self.sol.is_same_tree(p, q))

    def test_different_structure(self):
        # Tree 1: [1,2,1], Tree 2: [1,1,2]
        p = TreeNode(1, TreeNode(2), TreeNode(1))
        q = TreeNode(1, TreeNode(1), TreeNode(2))
        self.assertFalse(self.sol.is_same_tree(p, q))

    def test_both_empty(self):
        self.assertTrue(self.sol.is_same_tree(None, None))

    def test_one_empty(self):
        p = TreeNode(1)
        self.assertFalse(self.sol.is_same_tree(p, None))


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
