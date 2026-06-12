import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: BINARY SEARCH (EASY)  
--------------------------------------------------  
1. The Midpoint Formula: To avoid integer overflow in some languages, 
   mid = low + (high - low) // 2 is used. In Python 3, integers have 
   arbitrary precision, but this is still a good "Senior" habit to show.
2. Floor Division: Always use // for index calculation to ensure 
   the result is an integer.
3. While Condition: Use while low <= high: (not <) to ensure 
   you check the very last remaining element when the pointers meet.
4. bisect module: Python has a built-in 'bisect' library for binary search. 
   While great for production, interviewers usually want to see the 
   manual implementation first.
"""


class Solution:
    def binary_search(self, nums: List[int], target: int) -> int:
        """
        PROBLEM: BINARY SEARCH
        Given an array of integers nums which is sorted in ascending order,
        and an integer target, write a function to search target in nums.
        If target exists, then return its index. Otherwise, return -1.

        REQUIREMENTS:
        - You must write an algorithm with O(log n) runtime complexity.
        - Handle cases where the target is not present.
        - Space Complexity must be O(1).

        :param nums: A list of integers sorted in ascending order.
        :param target: The integer value to search for.
        :return: The index of target or -1.
        """
        min_idx = 0
        max_idx = len(nums) - 1

        # Time: O(log n) - search space halves with each iteration
        # Space: O(1) - only constant extra variables used
        while min_idx <= max_idx:
            mid_idx = min_idx + (max_idx - min_idx) // 2
            can = nums[mid_idx]
            if can == target:
                return mid_idx
            if can > target:
                max_idx = mid_idx - 1
            else:
                min_idx = mid_idx + 1

        return -1


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_case_1(self):
        # Target in the middle-ish
        self.assertEqual(self.sol.binary_search([-1, 0, 3, 5, 9, 12], 9), 4)

    def test_case_2(self):
        # Target not in the list
        self.assertEqual(self.sol.binary_search([-1, 0, 3, 5, 9, 12], 2), -1)

    def test_case_3(self):
        # Target is the first element
        self.assertEqual(self.sol.binary_search([5], 5), 0)

    def test_case_4(self):
        # Target is not the single element present
        self.assertEqual(self.sol.binary_search([5], -5), -1)

    def test_case_5(self):
        # Target is at the boundaries
        nums = [1, 2, 3, 4, 5]
        self.assertEqual(self.sol.binary_search(nums, 1), 0)
        self.assertEqual(self.sol.binary_search(nums, 5), 4)


if __name__ == "__main__":
    unittest.main()
