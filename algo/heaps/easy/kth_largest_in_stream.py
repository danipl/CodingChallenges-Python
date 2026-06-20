import heapq
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: HEAPS (EASY - BOUNDED HEAP)
----------------------------------------------------------
1. Bounded min-heap for Kth largest: Maintain a min-heap of size K. The root
   (smallest in the heap) is the Kth largest element overall. When adding a new
   element, push it; if heap size > K, pop the root. This keeps exactly the K
   largest elements seen so far.

2. Why min-heap (not max-heap)? A max-heap would give you the largest element,
   but you need the Kth largest. A min-heap of size K has the Kth largest at the
   root because all K elements are ≥ the root, and the root is the smallest of those K.

3. Streaming pattern: For "add and query" problems, store the heap as an instance
   variable. Each add() is O(log K), each query is O(1) — just peek at heap[0].

4. Initialization: When given an initial array, heapify the first K elements in O(K).
   Then for remaining elements, push and pop if size > K. Total: O(n log K).

5. heapq.nsmallest() / nlargest(): For one-shot queries, these are convenient.
   But for streaming (repeated add + query), maintaining your own heap is more efficient.
"""


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        """
        Initialize the KthLargest tracker.

        :param k: The Kth largest element to track (1-indexed, so k=1 means largest).
        :param nums: Initial list of integers.
        """
        self.k = k
        self.nums = nums
        # Time: O(n) - heapify converts list to heap in linear time
        heapq.heapify(self.nums)
        # Time: O((n-k) log n) - pop n-k times to trim to size k, each pop is O(log n)
        while len(self.nums) > k:
            heapq.heappop(self.nums)

        # Overall Time Complexity for __init__: O(n log n) - heapify O(n) + trimming O((n-k) log n)
        # Overall Space Complexity: O(k) - heap stores at most k elements

    def add(self, val: int) -> int:
        """
        Add a new value to the stream and return the Kth largest element.

        :param val: The integer to add.
        :return: The Kth largest element in the stream.
        """
        # Time: O(log k) - push maintains heap property
        heapq.heappush(self.nums, val)
        if len(self.nums) > self.k:
            # Time: O(log k) - pop maintains heap property
            heapq.heappop(self.nums)
        # Overall Time Complexity: O(log k) - push + potential pop
        # Overall Space Complexity: O(k) - heap stores at most k elements
        return self.nums[0]


class TestKthLargest(unittest.TestCase):
    def test_example_case(self):
        # k=3, initial=[4, 5, 8, 2]
        # After init: heap contains [4, 5, 8] (3 largest), 3rd largest = 4
        # add(3): heap becomes [3, 4, 8, 5] → pop 3 → [4, 5, 8], 3rd largest = 4
        # add(5): heap becomes [4, 5, 8, 5] → pop 4 → [5, 5, 8], 3rd largest = 5
        # add(10): heap becomes [5, 5, 8, 10] → pop 5 → [5, 8, 10], 3rd largest = 5
        # add(9): heap becomes [5, 8, 10, 9] → pop 5 → [8, 9, 10], 3rd largest = 8
        # add(4): heap becomes [4, 8, 10, 9] → pop 4 → [8, 9, 10], 3rd largest = 8
        kth = KthLargest(3, [4, 5, 8, 2])
        self.assertEqual(kth.add(3), 4)
        self.assertEqual(kth.add(5), 5)
        self.assertEqual(kth.add(10), 5)
        self.assertEqual(kth.add(9), 8)
        self.assertEqual(kth.add(4), 8)

    def test_k_equals_1(self):
        # k=1 means we always want the maximum
        kth = KthLargest(1, [])
        self.assertEqual(kth.add(3), 3)
        self.assertEqual(kth.add(5), 5)
        self.assertEqual(kth.add(2), 5)
        self.assertEqual(kth.add(10), 10)

    def test_initial_array_with_duplicates(self):
        # k=2, initial=[1, 1, 1, 1]
        # After init: heap contains [1, 1] (2 largest), 2nd largest = 1
        # add(1): heap becomes [1, 1, 1] → pop 1 → [1, 1], 2nd largest = 1
        kth = KthLargest(2, [1, 1, 1, 1])
        self.assertEqual(kth.add(1), 1)
        self.assertEqual(kth.add(2), 1)
        self.assertEqual(kth.add(3), 2)

    def test_small_initial_array(self):
        # k=3, initial=[1, 2] (fewer than k elements initially)
        # After init: heap=[1, 2], size < k, but we still track
        # add(3): heap=[1, 2, 3], size == k, 3rd largest = 1
        # add(4): heap=[1, 2, 3, 4] → pop 1 → [2, 3, 4], 3rd largest = 2
        # add(5): heap=[2, 3, 4, 5] → pop 2 → [3, 4, 5], 3rd largest = 3
        kth = KthLargest(3, [1, 2])
        self.assertEqual(kth.add(3), 1)
        self.assertEqual(kth.add(4), 2)
        self.assertEqual(kth.add(5), 3)

    def test_k_equals_n(self):
        # k=3, initial=[1, 2, 3]
        # After init: heap=[1, 2, 3], 3rd largest = 1
        # add(4): heap=[1, 2, 3, 4] → pop 1 → [2, 3, 4], 3rd largest = 2
        kth = KthLargest(3, [1, 2, 3])
        self.assertEqual(kth.add(4), 2)
        self.assertEqual(kth.add(5), 3)


if __name__ == "__main__":
    unittest.main()
