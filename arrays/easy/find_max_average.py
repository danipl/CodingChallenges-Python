import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: SLIDING WINDOW BASICS (EASY)  
------------------------------------------  
1. Fixed-Size Window: When the window size `k` is constant, calculate the 
   initial sum of the first `k` elements once.
2. The "Slide": To move the window, add the next element and subtract 
    the one that is no longer in the window. This keeps updates $O(1)$.
3. float('-inf'): Useful if the array contains negative numbers and you 
   need to track a maximum.
4. Precision: Python handles floating point division naturally with `/`, 
   but be careful with large numbers.
"""


class Solution:
    def find_max_average(self, nums: List[int], k: int) -> float:
        """
        PROBLEM: MAXIMUM AVERAGE SUBARRAY I
        You are given an integer array `nums` consisting of `n` elements,
        and an integer `k`.

        Find a contiguous subarray whose length is equal to `k` that has
        the maximum average value and return this value.

        REQUIREMENTS:
        - Return the maximum average as a float.
        - Time Complexity must be $O(n)$.
        - Space Complexity must be $O(1)$.

        :param nums: List of integers.
        :param k: Size of the subarray window.
        :return: Maximum average value.
        """
        current_sum = sum(nums[:k])  # Time: O(k), Space: O(1) - compute initial window sum
        max_sum = current_sum

        for idx in range(k, len(nums)):  # Time: O(n-k), Space: O(1) - iterate remaining elements
            current_sum += nums[idx] - nums[idx - k]
            max_sum = max(max_sum, current_sum)

        return max_sum / k


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard(self):
        # [12, -5, -6, 50] has sum 51. 51/4 = 12.75
        self.assertEqual(self.sol.find_max_average([1, 12, -5, -6, 50, 3], 4), 12.75)

    def test_single_element(self):
        self.assertEqual(self.sol.find_max_average([5], 1), 5.0)

    def test_all_negative(self):
        self.assertEqual(self.sol.find_max_average([-1], 1), -1.0)


if __name__ == "__main__":
    unittest.main()
