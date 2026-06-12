import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: LINKED LISTS (MEDIUM - BLIND 75)  
------------------------------------------  
1. Floyd’s Cycle-Finding Algorithm: Also known as "Tortoise and Hare." Use two pointers 
   moving at different speeds. If they meet, there is a cycle.
2. Identity Comparison: Use 'is' to check if two variables point to the same 
   object in memory (e.g., 'slow is fast').
3. Boolean Returns: Python handles 'True' and 'False' as first-class objects; 
   ensure your logic returns a clean bool.
4. Memory Efficiency: Cycle detection can be done in O(1) space, avoiding the 
   need for a hash set of visited nodes.
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:
    def has_cycle(self, head: Optional[ListNode]) -> bool:
        """
        PROBLEM: LINKED LIST CYCLE
        Given head, the head of a linked list, determine if the linked list
        has a cycle in it.

        REQUIREMENTS:
        - Return True if there is a cycle, False otherwise.
        - Time Complexity: O(n).
        - Space Complexity: O(1) (You must not use a Set or Hash Map).

        :param head: The head of the linked list.
        :return: Boolean indicating if a cycle exists.
        """
        if not head or not head.next:
            return False

        slow = head
        fast = head

        while fast and fast.next:  # Time: O(n) - traverse list once; Space: O(1) - only two pointers
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                return True

        # Overall Time Complexity: O(n) - we traverse the list at most once
        # Overall Space Complexity: O(1) - only using two pointers regardless of input size
        return False


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_cycle_exists(self):
        # 3 -> 2 -> 0 -> -4 -> (back to 2)
        node1 = ListNode(3)
        node2 = ListNode(2)
        node3 = ListNode(0)
        node4 = ListNode(-4)
        node1.next = node2
        node2.next = node3
        node3.next = node4
        node4.next = node2  # Cycle here
        self.assertTrue(self.sol.has_cycle(node1))

    def test_no_cycle(self):
        # 1 -> 2
        node1 = ListNode(1)
        node2 = ListNode(2)
        node1.next = node2
        self.assertFalse(self.sol.has_cycle(node1))

    def test_single_node_no_cycle(self):
        node1 = ListNode(1)
        self.assertFalse(self.sol.has_cycle(node1))

    def test_single_node_with_cycle(self):
        node1 = ListNode(1)
        node1.next = node1
        self.assertTrue(self.sol.has_cycle(node1))

    def test_empty_list(self):
        self.assertFalse(self.sol.has_cycle(None))


if __name__ == "__main__":
    unittest.main()
