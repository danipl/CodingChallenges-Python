import unittest
from typing import Optional

"""
PYTHON INTERVIEW CHEAT-SHEET: LINKED LISTS (EASY - FAST/SLOW POINTERS)
----------------------------------------------------------------------
1. Fast/Slow Pointer Pattern (Floyd's Algorithm): Use two pointers moving at
   different speeds. If there's a cycle, they'll eventually meet. If not, the
   fast pointer reaches the end. This is O(n) time, O(1) space.
2. Why it works: In a cycle, the fast pointer "laps" the slow pointer. Think of
   two runners on a circular track — the faster one will eventually catch up.
3. Meeting point detection: If slow == fast at any point during traversal, a
   cycle exists. If fast or fast.next becomes None, no cycle.
4. Common mistake: Don't check `if slow == fast` before moving — check AFTER
   advancing both pointers. Otherwise you'll miss cycles that start at head.
5. ListNode type hints: Always use `Optional[ListNode]` for nodes that can be None.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def has_cycle(self, head: Optional[ListNode]) -> bool:
        """
        PROBLEM: LINKED LIST CYCLE
        Given the head of a linked list, determine if the linked list has a cycle.

        A cycle occurs when a node can be reached again by continuously following
        the next pointer. The cycle is represented by an integer 'pos' which indicates
        the index (0-indexed) where the tail connects back to. If pos is -1, there is no cycle.

        REQUIREMENTS:
        - Return True if there is a cycle, False otherwise.
        - Must solve in O(n) time complexity.
        - Must solve in O(1) space complexity (no extra data structures).
        - Handle empty lists and single-node lists gracefully.

        :param head: The head of the linked list.
        :return: Boolean indicating if a cycle exists.

        Example 1:
            Input: head = [3, 2, 0, -4], pos = 1
            Output: True
            Explanation: Tail connects to node at index 1, creating a cycle.

        Example 2:
            Input: head = [1, 2], pos = -1
            Output: False
            Explanation: No cycle — tail points to None.

        Example 3:
            Input: head = [1], pos = -1
            Output: False
            Explanation: Single node with no cycle.

        Example 4:
            Input: head = [1, 2], pos = 0
            Output: True
            Explanation: Tail connects back to head, creating a cycle.
        """
        if not head:
            return False

        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True

        return False


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_no_cycle_linear(self):
        """Linear list: 1 -> 2 -> 3 -> None."""
        head = ListNode(1, ListNode(2, ListNode(3)))
        self.assertFalse(self.sol.has_cycle(head))

    def test_cycle_at_head(self):
        """Cycle: 1 -> 2 -> 3 -> back to 1."""
        node1 = ListNode(1)
        node2 = ListNode(2)
        node3 = ListNode(3)
        node1.next = node2
        node2.next = node3
        node3.next = node1  # cycle back to head
        self.assertTrue(self.sol.has_cycle(node1))

    def test_cycle_in_middle(self):
        """Cycle: 1 -> 2 -> 3 -> 4 -> back to 2."""
        node1 = ListNode(1)
        node2 = ListNode(2)
        node3 = ListNode(3)
        node4 = ListNode(4)
        node1.next = node2
        node2.next = node3
        node3.next = node4
        node4.next = node2  # cycle back to node2
        self.assertTrue(self.sol.has_cycle(node1))

    def test_single_node_no_cycle(self):
        """Single node pointing to None."""
        head = ListNode(1)
        self.assertFalse(self.sol.has_cycle(head))

    def test_single_node_with_cycle(self):
        """Single node pointing to itself."""
        head = ListNode(1)
        head.next = head
        self.assertTrue(self.sol.has_cycle(head))

    def test_empty_list(self):
        """Empty list — no cycle."""
        self.assertFalse(self.sol.has_cycle(None))

    def test_two_nodes_no_cycle(self):
        """Two nodes: 1 -> 2 -> None."""
        head = ListNode(1, ListNode(2))
        self.assertFalse(self.sol.has_cycle(head))

    def test_two_nodes_with_cycle(self):
        """Two nodes in cycle: 1 -> 2 -> 1."""
        node1 = ListNode(1)
        node2 = ListNode(2)
        node1.next = node2
        node2.next = node1
        self.assertTrue(self.sol.has_cycle(node1))


if __name__ == "__main__":
    unittest.main()
