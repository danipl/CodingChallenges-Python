import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (MEDIUM - KADANE'S ALGORITHM)
------------------------------------------
1. Kadane's Algorithm: Maintain a running sum (`current_sum`). At each element,
   decide: extend the previous subarray (`current_sum + num`) or start fresh (`num`).
   Formula: `current_sum = max(num, current_sum + num)`. Track the global max separately.
2. Negative Reset Insight: If `current_sum` becomes negative, it's strictly better
   to start a new subarray from the next element — a negative prefix only hurts.
3. Single-Pass Efficiency: The entire algorithm runs in O(n) time with O(1) space —
   no nested loops, no extra arrays. Just two variables.
4. Edge Case Handling: All-negative arrays are the trap. Initialize `max_sum` to
   `float('-inf')` or `nums[0]` — NOT 0 — so you correctly return the least negative
   element when no positive sum exists.
5. Variant Patterns: To find the subarray *indices* (not just the sum), track
   `start` and `end` pointers that update when you reset `current_sum` or beat `max_sum`.
"""


class Solution:
    def max_sub_array(self, nums: list[int]) -> int:
        """
        PROBLEM: MAXIMUM SUBARRAY
        Given an integer array 'nums', find the subarray with the largest sum,
        and return its sum.

        A subarray is a contiguous non-empty sequence of elements within an array.

        REQUIREMENTS:
        - Return the maximum sum of any contiguous subarray.
        - The array contains at least one element.
        - Elements can be negative, zero, or positive.
        - Time Complexity must be O(n) — single pass through the array.
        - Space Complexity must be O(1) — only a few variables.

        :param nums: A list of integers (at least one element).
        :return: The maximum contiguous subarray sum.

        Example 1:
            Input: nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
            Output: 6
            Explanation: The subarray [4, -1, 2, 1] has the largest sum = 6.

        Example 2:
            Input: nums = [1]
            Output: 1
            Explanation: The only subarray is [1], which has sum 1.

        Example 3:
            Input: nums = [5, 4, -1, 7, 8]
            Output: 23
            Explanation: The entire array has the largest sum.

        Example 4 (All Negative):
            Input: nums = [-3, -2, -5, -1]
            Output: -1
            Explanation: The subarray [-1] has the largest sum (least negative).
        """
        if not nums:
            return 0

        current_sum = nums[0]
        max_sum = current_sum

        # Time: O(n) - single pass through remaining elements
        for pos in range(1, len(nums)):
            num = nums[pos]
            current_sum = max(num, current_sum + num)
            max_sum = max(max_sum, current_sum)

        # Overall Time Complexity: O(n) - single pass, each element visited once
        # Overall Space Complexity: O(1) - only two integer variables
        return max_sum


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_mixed_positive_negative(self):
        """Classic case: positive subarray in the middle."""
        self.assertEqual(self.sol.max_sub_array([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)

    def test_single_element(self):
        """Minimal input — one element."""
        self.assertEqual(self.sol.max_sub_array([1]), 1)

    def test_all_positive(self):
        """Entire array is the best subarray."""
        self.assertEqual(self.sol.max_sub_array([5, 4, -1, 7, 8]), 23)

    def test_all_negative(self):
        """All negative — return the least negative element."""
        self.assertEqual(self.sol.max_sub_array([-3, -2, -5, -1]), -1)

    def test_single_negative(self):
        """Single negative element."""
        self.assertEqual(self.sol.max_sub_array([-1]), -1)

    def test_leading_negatives(self):
        """Negatives at the start, positive subarray later."""
        self.assertEqual(self.sol.max_sub_array([-1, -2, 3, 4, -5]), 7)

    def test_trailing_negatives(self):
        """Positive subarray at the start, negatives at the end."""
        self.assertEqual(self.sol.max_sub_array([3, 4, -5, -1, -2]), 7)

    def test_alternating_signs(self):
        """Alternating positive and negative values."""
        self.assertEqual(self.sol.max_sub_array([1, -1, 2, -2, 3, -3, 4]), 4)

    def test_large_positive_sum(self):
        """Large array with a clear maximum subarray."""
        self.assertEqual(self.sol.max_sub_array([0, 0, 0, 5, 5, 5, 0, 0]), 15)


if __name__ == "__main__":
    unittest.main()
