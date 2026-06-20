import unittest
from typing import Optional

"""
PYTHON INTERVIEW CHEAT-SHEET: LINKED LISTS (EASY - FINDING MIDDLE)
------------------------------------------------------------------
1. Fast/Slow Pointer for Middle: Move `slow` one step, `fast` two steps.
   When `fast` reaches the end, `slow` is at the middle. O(n) time, O(1) space.
2. Even vs Odd length: For even-length lists, there are two "middles". The standard
   is to return the SECOND middle (e.g., [1,2,3,4] → node 3, not node 2).
3. Loop condition: Use `while fast and fast.next:` to ensure `fast.next.next` is safe.
4. Alternative approaches: (1) Count nodes first, then traverse to n//2. (2) Use a
   stack to store nodes, then pop to middle. Both are O(n) time but O(n) space.
5. ListNode type hints: Always use `Optional[ListNode]` for nodes that can be None.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def middle_node(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        PROBLEM: MIDDLE OF LINKED LIST
        Given the head of a singly linked list, return the middle node.

        If there are two middle nodes (even-length list), return the SECOND middle node.

        REQUIREMENTS:
        - Return the middle node (not its value, but the node itself).
        - Must solve in O(n) time complexity.
        - Must solve in O(1) space complexity (no counting first, no extra data structures).
        - Handle single-node lists gracefully.

        :param head: The head of the linked list.
        :return: The middle node of the linked list.

        Example 1:
            Input: head = [1, 2, 3, 4, 5]
            Output: Node with value 3
            Explanation: The middle node of a 5-node list is the 3rd node.

        Example 2:
            Input: head = [1, 2, 3, 4, 5, 6]
            Output: Node with value 4
            Explanation: There are two middle nodes (3 and 4). Return the second one.

        Example 3:
            Input: head = [1]
            Output: Node with value 1
            Explanation: Single node is its own middle.
        """
        if not head:
            return None

        slow = fast = head

        # Time: O(n/2) = O(n) - fast advances 2 steps per iteration, loop runs ⌊n/2⌋ times
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Overall Time Complexity: O(n) - single pass through half the list
        # Overall Space Complexity: O(1) - two pointers only
        return slow


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_odd_length_middle(self):
        """List: 1 -> 2 -> 3 -> 4 -> 5. Middle is 3."""
        head = self._create_list([1, 2, 3, 4, 5])
        result = self.sol.middle_node(head)
        assert result is not None
        self.assertEqual(result.val, 3)
        self.assertEqual(self._list_from_node(result), [3, 4, 5])

    def test_even_length_second_middle(self):
        """List: 1 -> 2 -> 3 -> 4 -> 5 -> 6. Second middle is 4."""
        head = self._create_list([1, 2, 3, 4, 5, 6])
        result = self.sol.middle_node(head)
        assert result is not None
        self.assertEqual(result.val, 4)
        self.assertEqual(self._list_from_node(result), [4, 5, 6])

    def test_single_node(self):
        """List: 1. Middle is 1."""
        head = ListNode(1)
        result = self.sol.middle_node(head)
        assert result is not None
        self.assertEqual(result.val, 1)
        self.assertIsNone(result.next)

    def test_two_nodes(self):
        """List: 1 -> 2. Second middle is 2."""
        head = self._create_list([1, 2])
        result = self.sol.middle_node(head)
        assert result is not None
        self.assertEqual(result.val, 2)

    def test_three_nodes(self):
        """List: 1 -> 2 -> 3. Middle is 2."""
        head = self._create_list([1, 2, 3])
        result = self.sol.middle_node(head)
        assert result is not None
        self.assertEqual(result.val, 2)

    def test_four_nodes(self):
        """List: 1 -> 2 -> 3 -> 4. Second middle is 3."""
        head = self._create_list([1, 2, 3, 4])
        result = self.sol.middle_node(head)
        assert result is not None
        self.assertEqual(result.val, 3)

    def test_large_list(self):
        """List: 1 to 100. Middle is 51."""
        head = self._create_list(list(range(1, 101)))
        result = self.sol.middle_node(head)
        assert result is not None
        self.assertEqual(result.val, 51)

    def _create_list(self, values: list[int]) -> Optional[ListNode]:
        if not values:
            return None
        head = ListNode(values[0])
        current = head
        for val in values[1:]:
            current.next = ListNode(val)
            current = current.next
        return head

    def _list_from_node(self, node: Optional[ListNode]) -> list[int]:
        result = []
        while node:
            result.append(node.val)
            node = node.next
        return result


if __name__ == "__main__":
    unittest.main()
