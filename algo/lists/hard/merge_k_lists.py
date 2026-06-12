import heapq
import unittest
from typing import Optional, List

"""  
PYTHON INTERVIEW CHEAT-SHEET: HEAPS & MULTI-WAY MERGE (HARD)  
------------------------------------------  
1. heapq.heappush / heapq.heappop: Python's built-in min-heap. It only 
   works on the first element of a tuple. Use (node.val, i, node).
2. The Tie-Breaker: If two nodes have the same value, Python tries to compare 
   the 'ListNode' objects, which will crash. Always include a unique index 'i' 
   in your heap tuple: (val, index, node).
3. Space-Time Tradeoff: 
   - Heap: Time O(N log k), Space O(k).
   - Divide & Conquer: Time O(N log k), Space O(1) iterative.
4. Memory Efficiency: Since we are merging in-place, we only store 
   'k' pointers in the heap at any given time.
"""


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def merge_k_lists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        """
        PROBLEM: MERGE K SORTED LISTS
        You are given an array of k linked-lists 'lists', each linked-list
        is sorted in ascending order. Merge all the linked-lists into one
        sorted linked-list and return it.

        REQUIREMENTS:
        - Time Complexity: O(N log k), where N is total nodes and k is number of lists.
        - Space Complexity: O(k) for the heap.
        - Must handle empty lists and empty arrays gracefully.

        :param lists: A list of heads of sorted linked lists.
        :return: The head of the merged sorted linked list.
        """
        if len(lists) == 0:
            return None

        heap = []
        counter = 0

        # Time: O(k) - iterate through k lists once
        # Space: O(k) - heap stores at most k nodes
        for idx, l in enumerate(lists):
            if l:
                heapq.heappush(heap, (l.val, counter, l))
                counter += 1

        curr = head = ListNode()

        # Time: O(N log k) - N total nodes, each heap operation is O(log k)
        # Space: O(1) - only reusing existing nodes, heap size stays at O(k)
        while heap:
            val, _, node = heapq.heappop(heap)  # O(log k)
            curr.next = ListNode(val=val)
            curr = curr.next
            if node.next:
                heapq.heappush(heap, (node.next.val, counter, node.next))  # O(log k)
                counter += 1

        # Time: O(N log k) - Initial heap building is O(k log k), then N nodes
        # each require O(log k) for heap operations, dominated by O(N log k).
        # Space: O(k) - The heap maintains at most k nodes at any time.
        return head.next


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

    def test_three_lists(self):
        l1 = arr_to_list([1, 4, 5])
        l2 = arr_to_list([1, 3, 4])
        l3 = arr_to_list([2, 6])
        result = self.sol.merge_k_lists([l1, l2, l3])
        self.assertEqual(list_to_arr(result), [1, 1, 2, 3, 4, 4, 5, 6])

    def test_empty_input_array(self):
        result = self.sol.merge_k_lists([])
        self.assertEqual(list_to_arr(result), [])

    def test_array_with_empty_lists(self):
        result = self.sol.merge_k_lists([None, None])
        self.assertEqual(list_to_arr(result), [])

    def test_single_list(self):
        l1 = arr_to_list([1, 2, 3])
        result = self.sol.merge_k_lists([l1])
        self.assertEqual(list_to_arr(result), [1, 2, 3])

    def test_varied_lengths(self):
        l1 = arr_to_list([1])
        l2 = arr_to_list([1, 2])
        l3 = arr_to_list([3, 4, 5])
        result = self.sol.merge_k_lists([l1, l2, l3])
        self.assertEqual(list_to_arr(result), [1, 1, 2, 3, 4, 5])


if __name__ == "__main__":
    unittest.main()
