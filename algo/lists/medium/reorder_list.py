import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: THE LINKED LIST TRIATHLON (MEDIUM)  
------------------------------------------  
1. Fast/Slow Middle: 'slow' moves 1, 'fast' moves 2. When 'fast' ends, 'slow' 
   is at the middle. Useful for splitting lists.
2. In-Place Reversal: 'curr.next, prev, curr = prev, curr, curr.next' is your 
   bread and butter for flipping segments without extra space.
3. Interleaving: To merge 1->2 and 4->3 into 1->4->2->3, save next pointers 
   carefully before re-assigning: 'tmp1, tmp2 = l1.next, l2.next'.
4. None-Termination: When splitting a list, always set 'slow.next = None' 
   to officially break the connection between the first and second halves.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reorder_list(self, head: Optional[ListNode]) -> None:
        """
        PROBLEM: REORDER LIST
        You are given the head of a singly linked list: L0 → L1 → … → Ln - 1 → Ln
        Reorder the list to be on the following form: L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …

        REQUIREMENTS:
        - Modify the list IN-PLACE. Do not return anything.
        - Time Complexity: O(n).
        - Space Complexity: O(1).

        EXAMPLE:
        Input: 1 -> 2 -> 3 -> 4
        Output: 1 -> 4 -> 2 -> 3
        """
        if not head or not head.next:
            return head

        slow = fast = head

        # Step 1: Find middle using fast/slow pointers - O(n) time, O(1) space
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        prev = None
        curr = slow.next
        slow.next = None

        # Step 2: Reverse second half - O(n) time, O(1) space
        while curr:
            curr.next, prev, curr = prev, curr, curr.next

        first, second = head, prev
        # Step 3: Merge two halves - O(n) time, O(1) space
        while second:
            tmp1, tmp2 = first.next, second.next

            first.next = second
            second.next = tmp1

            first, second = tmp1, tmp2

        # Overall: Time Complexity O(n), Space Complexity O(1)


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

    def test_even_length(self):
        head = arr_to_list([1, 2, 3, 4])
        self.sol.reorder_list(head)
        self.assertEqual(list_to_arr(head), [1, 4, 2, 3])

    def test_odd_length(self):
        head = arr_to_list([1, 2, 3, 4, 5])
        self.sol.reorder_list(head)
        self.assertEqual(list_to_arr(head), [1, 5, 2, 4, 3])

    def test_two_nodes(self):
        head = arr_to_list([1, 2])
        self.sol.reorder_list(head)
        self.assertEqual(list_to_arr(head), [1, 2])

    def test_single_node(self):
        head = arr_to_list([1])
        self.sol.reorder_list(head)
        self.assertEqual(list_to_arr(head), [1])

    def test_empty(self):
        head = None
        self.sol.reorder_list(head)
        self.assertEqual(list_to_arr(head), [])


if __name__ == "__main__":
    unittest.main()
