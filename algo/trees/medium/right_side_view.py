import unittest
from collections import deque
from typing import Optional, List

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (RIGHT SIDE VIEW)  
--------------------------------------------------  
1. BFS for "Views": Level-order traversal is the most intuitive way to solve 
   "view" problems because each level contributes exactly one node to the result.
2. The 'Last Element' Logic: In a standard BFS level-loop, the last node 
   processed in the inner loop (for _ in range(level_size)) is the one visible 
   from the right.
3. Recursive Depth Tracking: Alternatively, a DFS can solve this by passing 
   the current depth and only adding a node to the result if it's the first 
   time that depth is reached (exploring Right before Left).
4. Deque Efficiency: As always, use collections.deque for O(1) pops.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def right_side_view(self, root: Optional[TreeNode]) -> List[int]:
        """
        PROBLEM: BINARY TREE RIGHT SIDE VIEW
        Given the root of a binary tree, imagine yourself standing on the
        right side of it. Return the values of the nodes you can see
        ordered from top to bottom.

        REQUIREMENTS:
        - Return a list of integers.
        - Time Complexity must be O(N).
        - Space Complexity must be O(D) where D is the diameter of the tree.

        :param root: Root of the binary tree.
        :return: List of integers seen from the right side.
        """
        if root is None:
            return []

        result = list()
        queue = deque()
        queue.append(root)

        while queue:  # O(N) time - visit each node once
            inserted = False
            level_size = len(queue)  # O(W) space - W is max width of tree
            for _ in range(level_size):
                curr = queue.popleft()
                if not inserted:
                    result.append(curr.val)
                    inserted = True
                if curr.right:
                    queue.append(curr.right)
                if curr.left:
                    queue.append(curr.left)

        # O(H) space - result contains H elements (height of tree)
        return result


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_tree(self):
        # Tree: [1,2,3,None,5,None,4] -> View: [1, 3, 4]
        root = TreeNode(1,
                        TreeNode(2, None, TreeNode(5)),
                        TreeNode(3, None, TreeNode(4)))
        self.assertEqual(self.sol.right_side_view(root), [1, 3, 4])

    def test_left_heavy_tree(self):
        # Tree: [1,2,None,3] -> View: [1, 2, 3] (3 is visible because nothing is to its right)
        root = TreeNode(1, TreeNode(2, TreeNode(3), None), None)
        self.assertEqual(self.sol.right_side_view(root), [1, 2, 3])

    def test_single_node(self):
        root = TreeNode(1)
        self.assertEqual(self.sol.right_side_view(root), [1])

    def test_empty_tree(self):
        self.assertEqual(self.sol.right_side_view(None), [])


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
