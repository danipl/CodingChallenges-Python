import heapq
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: HEAPS (EASY)
------------------------------------------
1. heapq module: Python's built-in min-heap. `heapq.heappush(heap, item)` adds
   in O(log n), `heapq.heappop(heap)` removes and returns the smallest in O(log n).
   The heap is just a regular list — heapq provides the functions to maintain heap order.

2. Negation trick for max-heap: Since heapq is min-heap only, negate values before
   pushing: `heapq.heappush(heap, -value)`. When popping, negate back: `-heapq.heappop(heap)`.
   This gives you max-heap behavior with no extra data structure.

3. heapify(): Convert a list into a heap in O(n) time with `heapq.heapify(lst)`.
   Much faster than pushing elements one by one (which would be O(n log n)).
   Use this when you have an existing list and need heap operations.

4. nlargest() / nsmallest(): For "top K" problems, `heapq.nlargest(k, iterable)` returns
   the k largest elements in O(n log k). Under the hood, it maintains a min-heap of size k.

5. Heap property: For min-heap, `heap[i] <= heap[2*i+1]` and `heap[i] <= heap[2*i+2]`.
   The smallest element is always at index 0. You never need to sort the entire list —
   just access heap[0] for the minimum.
"""


class Solution:
    def lastStoneWeight(self, stones: list[int]) -> int:
        """
        PROBLEM: LAST STONE WEIGHT

        You are given an array of integers representing the weights of stones.

        Each turn, we choose the two heaviest stones and smash them together.
        Suppose the stones have weights x and y with x <= y. The result of this
        smash is:
        - If x == y, both stones are totally destroyed.
        - If x != y, the stone of weight x is totally destroyed, and the stone
          of weight y gets new weight y - x.

        At the end, there is at most 1 stone left. Return the weight of this
        stone (or 0 if no stones remain).

        REQUIREMENTS:
        - Return the weight of the last remaining stone, or 0 if none remain.
        - Time Complexity must be O(n log n).
        - Space Complexity must be O(n) for the heap.
        - Hint: You need to repeatedly extract the TWO maximum elements.

        :param stones: List of positive integers (stone weights).
        :return: Weight of last stone, or 0.
        """
        if not stones:
            return 0

        # Space: O(n) - new list with negated values for max-heap simulation
        stones = [-x for x in stones]

        # Time: O(n) - heapify is faster than n individual pushes
        heapq.heapify(stones)

        # Time: O(n log n) - at most n-1 iterations, each with O(log n) heap ops
        while len(stones) > 1:
            # Time: O(log n) - pop and re-heapify
            heaviest = abs(heapq.heappop(stones))
            second_heaviest = abs(heapq.heappop(stones))
            if heaviest != second_heaviest:
                # Time: O(log n) - push result back into heap
                heapq.heappush(stones, -(heaviest - second_heaviest))

        # Overall Time Complexity: O(n log n) - heapify O(n) + n iterations of O(log n)
        # Overall Space Complexity: O(n) - heap stores up to n elements
        return abs(heapq.heappop(stones)) if stones else 0


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_example_case(self):
        # Stones: [2, 7, 4, 1, 8, 1]
        # Smash 8 and 7 → 1 remains. Stones: [2, 4, 1, 1, 1]
        # Smash 4 and 2 → 2 remains. Stones: [1, 1, 1, 2]
        # Smash 2 and 1 → 1 remains. Stones: [1, 1, 1]
        # Smash 1 and 1 → 0 remain. Stones: [1]
        # Result: 1
        self.assertEqual(self.sol.lastStoneWeight([2, 7, 4, 1, 8, 1]), 1)

    def test_two_equal_stones(self):
        # Two stones of equal weight destroy each other
        self.assertEqual(self.sol.lastStoneWeight([5, 5]), 0)

    def test_two_different_stones(self):
        # 10 - 3 = 7 remains
        self.assertEqual(self.sol.lastStoneWeight([3, 10]), 7)

    def test_single_stone(self):
        # Only one stone, no smashing possible
        self.assertEqual(self.sol.lastStoneWeight([42]), 42)

    def test_empty_array(self):
        # No stones at all
        self.assertEqual(self.sol.lastStoneWeight([]), 0)

    def test_all_same_weight(self):
        # [3, 3, 3, 3] → smash pairs: (3,3)→0, (3,3)→0 → result 0
        self.assertEqual(self.sol.lastStoneWeight([3, 3, 3, 3]), 0)

    def test_descending_order(self):
        # Already sorted descending — should still work
        # [10, 8, 6, 4, 2]
        # Smash 10, 8 → 2. Stones: [6, 4, 2, 2]
        # Smash 6, 4 → 2. Stones: [2, 2, 2]
        # Smash 2, 2 → 0. Stones: [2]
        # Result: 2
        self.assertEqual(self.sol.lastStoneWeight([10, 8, 6, 4, 2]), 2)


if __name__ == "__main__":
    unittest.main()
