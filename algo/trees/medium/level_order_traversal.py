import unittest
from collections import deque
from typing import Optional, List

"""  
PYTHON INTERVIEW CHEAT-SHEET: TREES (MEDIUM - BFS)  
--------------------------------------------------  
1. collections.deque: Always use this for queues. 'popleft()' is O(1), 
   whereas 'list.pop(0)' is O(N).
2. Level Processing Pattern: Use 'for _ in range(len(queue))' inside the 
   'while queue' loop to process one full level at a time.
3. List Comprehensions: Useful for converting a level of nodes into a 
   list of integers quickly: [node.val for node in current_level].
4. Memory Management: BFS space complexity is O(W), where W is the 
   maximum width of the tree.
"""


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def level_order_traversal(self, root: Optional[TreeNode]) -> List[List[int]]:
        """
        PROBLEM: BINARY TREE LEVEL ORDER TRAVERSAL
        Given the root of a binary tree, return the level order traversal
        of its nodes' values (i.e., from left to right, level by level).

        REQUIREMENTS:
        - Return a list of lists, where each inner list represents a level.
        - Must handle empty trees (return []).
        - Time Complexity must be O(N).
        - Space Complexity must be O(N) (to hold the queue and the result).

        :param root: Root of the binary tree.
        :return: List of levels of integers.
        """
        if root is None:
            return []

        result = list()
        queue = deque()
        queue.append(root)

        # Time: O(N) - visit each node once
        # Space: O(W) - max width of tree in queue
        while queue:
            temp = list()
            el_nums = len(queue)
            for _ in range(el_nums):
                current = queue.popleft()
                temp.append(current.val)
                if current.left is not None:
                    queue.append(current.left)
                if current.right is not None:
                    queue.append(current.right)
            result.append(temp)

        # Overall: Time O(N)
        # Space O(N) for result + O(W) for queue
        return result


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_tree(self):
        # Tree: [3,9,20,None,None,15,7]
        # Levels: [[3], [9,20], [15,7]]
        root = TreeNode(3,
                        TreeNode(9),
                        TreeNode(20, TreeNode(15), TreeNode(7)))
        expected = [[3], [9, 20], [15, 7]]
        self.assertEqual(self.sol.level_order_traversal(root), expected)

    def test_single_node(self):
        root = TreeNode(1)
        self.assertEqual(self.sol.level_order_traversal(root), [[1]])

    def test_empty_tree(self):
        self.assertEqual(self.sol.level_order_traversal(None), [])

    def test_unbalanced_tree(self):
        # Tree: [1,2,None,3,None,4]
        # Levels: [[1], [2], [3], [4]]
        root = TreeNode(1, TreeNode(2, TreeNode(3, TreeNode(4))))
        expected = [[1], [2], [3], [4]]
        self.assertEqual(self.sol.level_order_traversal(root), expected)


if __name__ == "__main__":
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
