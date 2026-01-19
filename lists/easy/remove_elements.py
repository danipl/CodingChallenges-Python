import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: NODE DELETION (EASY/MEDIUM)  
------------------------------------------  
1. The Dummy Node: Your ultimate defense! Starting with 'dummy.next = head' 
   allows you to delete the original head without special 'if' logic.
2. The "Stay Put" Pointer: When you delete 'curr.next', do NOT move 'curr' 
   forward immediately. The new 'curr.next' also needs to be checked!
3. Garbage Collection: In Python, simply removing the reference 
   (curr.next = curr.next.next) is sufficient for deletion.
4. While curr.next: This loop style is best for deletion because it gives 
   you access to the node *before* the one you might remove.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def remove_elements(self, head: Optional[ListNode], val: int) -> Optional[ListNode]:
        """
        PROBLEM: REMOVE LINKED LIST ELEMENTS
        Given the head of a linked list and an integer val, remove all the
        nodes of the linked list that has Node.val == val, and return the new head.

        REQUIREMENTS:
        - Return the head of the modified list.
        - Handle cases where the target value is at the head, tail, or repeats.
        - Time Complexity: O(n).
        - Space Complexity: O(1).

        EXAMPLE:
        Input: 1 -> 2 -> 6 -> 3 -> 4 -> 5 -> 6, val = 6
        Output: 1 -> 2 -> 3 -> 4 -> 5
        """
        if not head or not head.next:
            return head

        dummy = ListNode(next=head)
        curr = dummy

        # Time: O(n) - visit each node once
        # Space: O(1) - only pointers, no extra data structures
        while curr and curr.next:
            if curr.next.val == val:
                curr.next = curr.next.next
            else:
                curr = curr.next

        # Overall: Time O(n), Space O(1)
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

    def test_middle_and_tail(self):
        head = arr_to_list([1, 2, 6, 3, 4, 5, 6])
        result = self.sol.remove_elements(head, 6)
        self.assertEqual(list_to_arr(result), [1, 2, 3, 4, 5])

    def test_all_elements_match(self):
        head = arr_to_list([7, 7, 7, 7])
        result = self.sol.remove_elements(head, 7)
        self.assertEqual(list_to_arr(result), [])

    def test_head_matches(self):
        head = arr_to_list([1, 2, 3])
        result = self.sol.remove_elements(head, 1)
        self.assertEqual(list_to_arr(result), [2, 3])

    def test_empty_list(self):
        result = self.sol.remove_elements(None, 1)
        self.assertEqual(list_to_arr(result), [])

    def test_no_matches(self):
        head = arr_to_list([1, 2, 3])
        result = self.sol.remove_elements(head, 4)
        self.assertEqual(list_to_arr(result), [1, 2, 3])


if __name__ == "__main__":
    unittest.main()
