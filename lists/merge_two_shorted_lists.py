import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: MERGING LISTS (EASY/MEDIUM)  
------------------------------------------  
1. The Dummy Node: Essential here! Initialize 'dummy = ListNode(0)' to act as 
   the starting point of your new list. It prevents "if not head" logic.
2. While L1 and L2: Use a loop that continues only as long as both lists have 
   nodes. This is where the primary comparison happens.
3. The "Tail" Cleanup: After the loop, one list might still have nodes. Use 
   'curr.next = l1 or l2' to attach the remaining segment in O(1) time.
4. Pointer Coordination: You'll manage three pointers—one for each input list 
   and one to track the tail of the new merged list.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def merge_two_shorted_lists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        """
        PROBLEM: MERGE TWO SORTED LISTS
        Merge two sorted linked lists and return it as a sorted list. The list
        should be made by splicing together the nodes of the first two lists.

        REQUIREMENTS:
        - Return the head of the new merged list.
        - Must be done in-place (reuse the existing nodes).
        - Time Complexity: O(n + m).
        - Space Complexity: O(1).

        :param list1: Head of the first sorted list.
        :param list2: Head of the second sorted list.
        :return: Head of the merged sorted list.
        """
        if not list1:
            return list2
        if not list2:
            return list1

        curr = ListNode()
        dummy = curr

        while list1 and list2:  # O(min(n, m)) time - iterate until one list is exhausted
            if list1.val <= list2.val:
                curr.next = list1
                list1 = list1.next
            else:
                curr.next = list2
                list2 = list2.next

            curr = curr.next

        if list1:
            curr.next = list1
        else:
            curr.next = list2

        # Overall Time Complexity: O(n + m) where n and m are lengths of list1 and list2
        # Overall Space Complexity: O(1) - only using constant extra space (pointers)
        return dummy.next


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

    def test_standard_merge(self):
        l1 = arr_to_list([1, 2, 4])
        l2 = arr_to_list([1, 3, 4])
        merged = self.sol.merge_two_shorted_lists(l1, l2)
        self.assertEqual(list_to_arr(merged), [1, 1, 2, 3, 4, 4])

    def test_different_lengths(self):
        l1 = arr_to_list([1, 2])
        l2 = arr_to_list([3, 4, 5, 6])
        merged = self.sol.merge_two_shorted_lists(l1, l2)
        self.assertEqual(list_to_arr(merged), [1, 2, 3, 4, 5, 6])

    def test_one_empty(self):
        l1 = arr_to_list([])
        l2 = arr_to_list([0])
        merged = self.sol.merge_two_shorted_lists(l1, l2)
        self.assertEqual(list_to_arr(merged), [0])

    def test_both_empty(self):
        merged = self.sol.merge_two_shorted_lists(None, None)
        self.assertEqual(list_to_arr(merged), [])

    def test_negative_values(self):
        l1 = arr_to_list([-10, -5, 0])
        l2 = arr_to_list([-7, 2])
        merged = self.sol.merge_two_shorted_lists(l1, l2)
        self.assertEqual(list_to_arr(merged), [-10, -7, -5, 0, 2])


if __name__ == "__main__":
    unittest.main()
