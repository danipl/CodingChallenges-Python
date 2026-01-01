import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: LINKED LISTS (EASY)  
------------------------------------------  
1. Optional[ListNode]: Use this type hint from 'typing' for nodes that can be None.
2. Multiple Assignment: Use 'a.next, b.next = b, a' for clean pointer swaps.
3. Sentinel/Dummy Nodes: Use 'dummy = ListNode(0, head)' to simplify edge cases 
   like deleting the head or inserting at the start.
4. Fast & Slow Pointers: A classic pattern for finding the middle or detecting cycles.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverse_list(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """
        PROBLEM: REVERSE A SINGLY LINKED LIST
        Given the head of a singly linked list, reverse the list, and return
        the reversed list.

        REQUIREMENTS:
        - Return the new head of the reversed list.
        - Handle lists with 0 or 1 nodes gracefully.
        - Time Complexity must be O(n).
        - Space Complexity must be O(1) for iterative.

        :param head: The head of the linked list.
        :return: The new head of the reversed list.
        """
        if not head:
            return None

        prv = None
        current = head

        # O(n) time total - iterates through all n nodes
        while current:
            nxt = current.next
            current.next = prv
            prv = current
            current = nxt

        # Overall: O(n) time, O(1) space - return new head of reversed list
        return prv


# --- Helper Methods for Testing ---

def list_to_arr(node: Optional[ListNode]) -> list[int]:
    result = []
    while node:
        result.append(node.val)
        node = node.next
    return result


def arr_to_list(arr: list[int]) -> Optional[ListNode]:
    if not arr: return None
    head = ListNode(arr[0])
    curr = head
    for i in range(1, len(arr)):
        curr.next = ListNode(arr[i])
        curr = curr.next
    return head


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_list(self):
        head = arr_to_list([1, 2, 3, 4, 5])
        reversed_head = self.sol.reverse_list(head)
        self.assertEqual(list_to_arr(reversed_head), [5, 4, 3, 2, 1])

    def test_two_elements(self):
        head = arr_to_list([1, 2])
        reversed_head = self.sol.reverse_list(head)
        self.assertEqual(list_to_arr(reversed_head), [2, 1])

    def test_single_element(self):
        head = arr_to_list([1])
        reversed_head = self.sol.reverse_list(head)
        self.assertEqual(list_to_arr(reversed_head), [1])

    def test_empty_list(self):
        head = arr_to_list([])
        reversed_head = self.sol.reverse_list(head)
        self.assertEqual(list_to_arr(reversed_head), [])

    def test_large_list(self):
        vals = list(range(100))
        head = arr_to_list(vals)
        reversed_head = self.sol.reverse_list(head)
        self.assertEqual(list_to_arr(reversed_head), vals[::-1])


if __name__ == "__main__":
    unittest.main()
