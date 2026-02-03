import unittest

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (MEDIUM - RECURSION)  
------------------------------------------------------  
1. Divide and Conquer: LCA is often solved by asking the left child and 
   right child for information and combining the results at the parent.
2. Return 'None' as a Signal: In recursion, returning 'None' can signal 
   that a target node was not found in a specific subtree.
3. Boolean Logic in Trees: If 'left_result' and 'right_result' both exist, 
   it means the current node MUST be the ancestor.
4. Identity over Equality: Use 'if root is p' (identity) instead of 
   'if root == p' (value equality) when dealing with specific node objects.
"""


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution:
    def lowest_common_ancestor(self, root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':
        """
        PROBLEM: LOWEST COMMON ANCESTOR OF A BINARY TREE
        Given a binary tree, find the lowest common ancestor (LCA) of two
        given nodes, p and q. The LCA is defined as the lowest node in T
        that has both p and q as descendants (where we allow a node to
        be a descendant of itself).

        REQUIREMENTS:
        - p and q will exist in the tree.
        - Time Complexity must be O(N).
        - Space Complexity must be O(H).

        :param root: The root of the tree.
        :param p: First target node.
        :param q: Second target node.
        :return: The TreeNode that is the LCA.
        """
        if root is None or root is p or root is q:
            return root

        # Time: O(N) - visit each node once in worst case
        # Space: O(H) - recursion stack depth equals tree height
        l_ancestor = self.lowest_common_ancestor(root.left, p, q)
        r_ancestor = self.lowest_common_ancestor(root.right, p, q)

        if l_ancestor and r_ancestor:
            return root

        # Otherwise, return whichever subtree found a node (or None if neither did)
        return l_ancestor if l_ancestor else r_ancestor


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_lca(self):
        # Tree: [3,5,1,6,2,0,8,None,None,7,4]
        # p = 5, q = 1 -> LCA = 3
        root = TreeNode(3)
        node5 = TreeNode(5)
        node1 = TreeNode(1)
        root.left = node5
        root.right = node1
        node5.left = TreeNode(6)
        node5.right = TreeNode(2)
        node1.left = TreeNode(0)
        node1.right = TreeNode(8)

        self.assertEqual(self.sol.lowest_common_ancestor(root, node5, node1), root)

    def test_node_is_own_ancestor(self):
        # p = 5, q = 4 -> LCA = 5
        root = TreeNode(3)
        node5 = TreeNode(5)
        node4 = TreeNode(4)
        root.left = node5
        node5.right = TreeNode(2)
        node5.right.right = node4

        self.assertEqual(self.sol.lowest_common_ancestor(root, node5, node4), node5)

    def test_different_branches(self):
        # p = 6, q = 4 -> LCA = 5
        root = TreeNode(3)
        node5 = TreeNode(5)
        node6 = TreeNode(6)
        node4 = TreeNode(4)
        root.left = node5
        node5.left = node6
        node5.right = TreeNode(2)
        node5.right.right = node4

        self.assertEqual(self.sol.lowest_common_ancestor(root, node6, node4), node5)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
