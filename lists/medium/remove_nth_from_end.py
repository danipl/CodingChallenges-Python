import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: TWO-POINTER GAP (MEDIUM)  
------------------------------------------  
1. The "Fast/Slow Gap": To find the N-th node from the end, move a 'fast' 
   pointer N steps ahead. Then move 'fast' and 'slow' at the same speed. 
   When 'fast' hits the end, 'slow' will be at the correct spot.
2. Dummy Nodes (Again!): Crucial here. If you need to remove the head, 
   a dummy node ensures 'slow' can always stay *behind* the node to be deleted.
3. Memory Management: In Python, you just change the pointer (prev.next = prev.next.next) 
   and the garbage collector handles the rest.
4. Edge Case - List of 1: Removing the only node should return None.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def remove_nth_from_end(self, head: Optional[ListNode], n: int) -> Optional[ListNode]:
        """
        PROBLEM: REMOVE N-TH NODE FROM END OF LIST
        Given the head of a linked list, remove the n-th node from the end
        of the list and return its head.

        REQUIREMENTS:
        - Return the head of the modified list.
        - Must be done in ONE pass.
        - Time Complexity: O(L) where L is list length.
        - Space Complexity: O(1).

        :param head: Head of the linked list.
        :param n: Position from the end (1-indexed).
        :return: Head of the modified list.
        """
        if not head:
            return head

        dummy = ListNode(next=head)

        slow = curr = dummy

        for _ in range(n):  # O(n) time - move curr pointer n steps ahead
            curr = curr.next
            if not curr:
                return None

        while curr.next:  # O(L-n) time - traverse remaining list until curr reaches end
            curr = curr.next
            slow = slow.next

        slow.next = slow.next.next if slow.next else None

        # Overall Time Complexity: O(L) where L is the length of the list
        # - First loop: O(n) to move curr pointer n steps ahead
        # - Second loop: O(L-n) to traverse remaining list
        # - Total: O(n) + O(L-n) = O(L)
        # Overall Space Complexity: O(1) - only using constant extra space (dummy, slow, curr pointers)

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

    def test_remove_middle(self):
        # 1 -> 2 -> 3 -> 4 -> 5, n = 2 => 1 -> 2 -> 3 -> 5
        head = arr_to_list([1, 2, 3, 4, 5])
        result = self.sol.remove_nth_from_end(head, 2)
        self.assertEqual(list_to_arr(result), [1, 2, 3, 5])

    def test_remove_head(self):
        # 1 -> 2, n = 2 => 2
        head = arr_to_list([1, 2])
        result = self.sol.remove_nth_from_end(head, 2)
        self.assertEqual(list_to_arr(result), [2])

    def test_remove_tail(self):
        # 1 -> 2, n = 1 => 1
        head = arr_to_list([1, 2])
        result = self.sol.remove_nth_from_end(head, 1)
        self.assertEqual(list_to_arr(result), [1])

    def test_single_node(self):
        # 1, n = 1 => []
        head = arr_to_list([1])
        result = self.sol.remove_nth_from_end(head, 1)
        self.assertEqual(list_to_arr(result), [])

    def test_remove_from_long_list(self):
        head = arr_to_list(list(range(10)))  # 0-9
        result = self.sol.remove_nth_from_end(head, 7)  # removes '3'
        self.assertEqual(list_to_arr(result), [0, 1, 2, 4, 5, 6, 7, 8, 9])


if __name__ == "__main__":
    unittest.main()
