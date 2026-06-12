import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY)  
-------------------------------------------------  
1. In-place vs. New List: When you need to build a result based on 
   comparisons from both ends of an array, initializing a result list 
   of a fixed size `[0] * n` is often more efficient than `.append()`.
2. Absolute Values: `abs(x)` is useful when comparing magnitudes of 
   negative and positive numbers in a sorted list.
3. reverse() and [::-1]: Sometimes it's easier to build a list 
   backwards and reverse it, but for this problem, filling from the 
   end of the result array is the "Elite" way to do it.
4. Memory Management: Python's `** 2` or `x * x` are both fine for 
   squaring; `x * x` is technically a tiny bit faster.
"""


class Solution:
    def sorted_squares(self, nums: List[int]) -> List[int]:
        """
        PROBLEM: SQUARES OF A SORTED ARRAY
        Given an integer array nums sorted in non-decreasing order,
        return an array of the squares of each number sorted in non-decreasing order.

        Example:
        Input: [-4, -1, 0, 3, 10]
        Output: [0, 1, 9, 16, 100]
        Explanation: After squaring, the array becomes [16, 1, 0, 9, 100].
        After sorting, it becomes [0, 1, 9, 16, 100].

        REQUIREMENTS:
        - You must achieve O(n) time complexity.
          (Note: Squaring and then using .sort() is O(n log n)).
        - Space Complexity should be O(n) for the output array.

        :param nums: A list of integers sorted in ascending order.
        :return: A list of the squares in ascending order.
        """
        left_idx, right_idx = 0, len(nums) - 1
        result = [0] * len(nums)  # O(n) time, O(n) space - Create result array of size n
        pos_idx = len(result) - 1

        while left_idx <= right_idx:  # O(n) time total, O(1) space - Loop through array once
            left = nums[left_idx]
            right = nums[right_idx]
            if abs(left) < abs(right):
                result[pos_idx] = right ** 2
                right_idx -= 1
            else:
                result[pos_idx] = left ** 2
                left_idx += 1

            pos_idx -= 1

        return result

        # Time: O(n) where n is the length of nums
        # Space: O(n) where n is the length of nums


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_case_1(self):
        # Mixed negative and positive
        self.assertEqual(self.sol.sorted_squares([-4, -1, 0, 3, 10]), [0, 1, 9, 16, 100])

    def test_case_2(self):
        # All negative
        self.assertEqual(self.sol.sorted_squares([-7, -3, -2, -1]), [1, 4, 9, 49])

    def test_case_3(self):
        # All positive
        self.assertEqual(self.sol.sorted_squares([1, 2, 3, 4]), [1, 4, 9, 16])

    def test_case_4(self):
        # Single element
        self.assertEqual(self.sol.sorted_squares([-5]), [25])

    def test_case_5(self):
        # Duplicate values
        self.assertEqual(self.sol.sorted_squares([-2, -2, 1, 1]), [1, 1, 4, 4])


if __name__ == "__main__":
    unittest.main()
