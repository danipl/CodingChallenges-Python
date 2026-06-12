import unittest
from typing import Optional

"""  
PYTHON INTERVIEW CHEAT-SHEET: ROTATION & MODULO (MEDIUM)  
------------------------------------------  
1. Modulo for K: If k is larger than the list length (L), rotating k times 
   is the same as rotating k % L times. Always calculate length first!
2. Creating a Ring: A common trick for rotation is to connect the tail back 
   to the head to form a circle, then break the circle at the new tail.
3. Finding the New Tail: If the list has length L, the new tail after 
   rotating k times is at position (L - k % L - 1) from the start.
4. Edge Case Handling: If k=0 or k is a multiple of L, the list doesn't change.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def rotate_right(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """
        PROBLEM: ROTATE LIST
        Given the head of a linked list, rotate the list to the right by k places.

        REQUIREMENTS:
        - Return the new head.
        - Handle k >= list length.
        - Time Complexity: O(n).
        - Space Complexity: O(1).

        EXAMPLE:
        Input: 1 -> 2 -> 3 -> 4 -> 5, k = 2
        Output: 4 -> 5 -> 1 -> 2 -> 3
        """
        if k == 0 or not head:
            return head

        curr = head
        length = 1

        # O(n) time - traverse entire list to find length
        while curr.next:
            length += 1
            curr = curr.next

        tail = curr

        pos = k % length

        if pos == 0:
            return head

        curr = head

        # O(n) time - traverse to new tail position
        for _ in range(length - pos - 1):
            curr = curr.next

        tail.next = head
        head = curr.next
        curr.next = None

        # Overall time: O(n), Overall space: O(1)
        return head


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

    def test_standard_rotation(self):
        head = arr_to_list([1, 2, 3, 4, 5])
        result = self.sol.rotate_right(head, 2)
        self.assertEqual(list_to_arr(result), [4, 5, 1, 2, 3])

    def test_k_greater_than_length(self):
        head = arr_to_list([0, 1, 2])
        result = self.sol.rotate_right(head, 4)  # same as k=1
        self.assertEqual(list_to_arr(result), [2, 0, 1])

    def test_zero_rotation(self):
        head = arr_to_list([1, 2])
        result = self.sol.rotate_right(head, 0)
        self.assertEqual(list_to_arr(result), [1, 2])

    def test_empty_list(self):
        result = self.sol.rotate_right(None, 5)
        self.assertEqual(list_to_arr(result), [])

    def test_single_node(self):
        head = arr_to_list([1])
        result = self.sol.rotate_right(head, 99)
        self.assertEqual(list_to_arr(result), [1])


if __name__ == "__main__":
    unittest.main()
