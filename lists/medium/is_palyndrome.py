import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: PALINDROME PATTERNS (EASY/MEDIUM)  
------------------------------------------  
1. The "List Copy" Trap: Converting a linked list to an array costs O(n) space. 
   An interviewer will almost always ask for O(1) space to test your pointer skills.
2. The Strategy: 1. Find the middle. 2. Reverse the second half. 3. Compare 
   the two halves node-by-node. 4. (Optional) Reverse back to restore the list.
3. Fast/Slow for Odd Lengths: If 'fast' is not None at the end, the list has an 
   odd number of nodes; 'slow' will be exactly at the center.
4. Careful Comparisons: 'while head2:' is usually better than 'while head1 and head2' 
   if the first half is slightly longer due to an odd total count.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def is_palindrome(self, head: Optional[ListNode]) -> bool:
        """
        PROBLEM: PALINDROME LINKED LIST
        Given the head of a singly linked list, return true if it is a palindrome.

        REQUIREMENTS:
        - Return True or False.
        - Time Complexity: O(n).
        - Space Complexity: O(1).

        EXAMPLE:
        Input: 1 -> 2 -> 2 -> 1  => Output: True
        Input: 1 -> 2 -> 3       => Output: False
        """
        if not head or not head.next:
            return True

        dummy = ListNode()
        dummy.next = head

        slow = fast = dummy

        # Step 1: Find middle using fast/slow pointers - O(n) time, O(1) space
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        current = slow.next
        slow.next = None
        prev = None

        # Step 2: Reverse second half - O(n) time, O(1) space
        while current:
            nxt = current.next
            current.next = prev
            prev = current
            current = nxt

        list1 = head
        list2 = prev

        # Step 3: Compare two halves - O(n) time, O(1) space
        while list2:
            if list1.val != list2.val:
                return False
            list1 = list1.next
            list2 = list2.next

        # Overall: Time Complexity O(n), Space Complexity O(1)
        return True


# --- Helper Methods for Testing ---
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

    def test_even_palindrome(self):
        head = arr_to_list([1, 2, 2, 1])
        self.assertTrue(self.sol.is_palindrome(head))

    def test_odd_palindrome(self):
        head = arr_to_list([1, 2, 3, 2, 1])
        self.assertTrue(self.sol.is_palindrome(head))

    def test_not_palindrome(self):
        head = arr_to_list([1, 2, 3])
        self.assertFalse(self.sol.is_palindrome(head))

    def test_single_node(self):
        head = arr_to_list([1])
        self.assertTrue(self.sol.is_palindrome(head))

    def test_two_different_nodes(self):
        head = arr_to_list([1, 2])
        self.assertFalse(self.sol.is_palindrome(head))


if __name__ == "__main__":
    unittest.main()
