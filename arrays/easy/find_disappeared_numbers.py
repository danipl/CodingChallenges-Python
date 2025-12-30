import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: IN-PLACE MAPPING (EASY/MED)  
--------------------------------------------------------  
1. Index as Hash Key: Since the values are in range [1, n] and the 
   indices are [0, n-1], we can treat the value `x` as pointing 
   to index `x-1`.
2. Sign Flipping Trick: To "mark" that we have seen a number `x`, 
   we can go to index `abs(x)-1` and make the value there negative. 
   `nums[idx] = -abs(nums[idx])`.
3. abs() is Critical: When traversing, always use `abs(nums[i])` 
   because a previous step might have already flipped the current 
   number to negative.
4. Second Pass: After marking, any index `i` that still has a 
   positive value means the number `i+1` was never seen.
"""


class Solution:
    def find_disappeared_numbers(self, nums: List[int]) -> List[int]:
        """
        PROBLEM: FIND ALL NUMBERS DISAPPEARED IN AN ARRAY
        Given an array nums of n integers where nums[i] is in the range [1, n],
        return an array of all the integers in the range [1, n] that
        do not appear in nums.

        REQUIREMENTS:
        - Time Complexity: O(n).
        - Space Complexity: O(1) (excluding the returned list).
        - You must not use extra space like a set or a dictionary.

        :param nums: List of integers in range [1, n].
        :return: List of missing integers.
        """
        # Time: O(n), Space: O(1) - Mark presence by negating value at index (val-1)
        for val in nums:
            val = abs(val)
            nums[val - 1] = -abs(nums[val - 1])

        # Time: O(n), Space: O(n) - Collect numbers whose indices remain positive
        disappeared_numbers = []
        for val in range(1, len(nums) + 1):
            idx = val - 1
            if nums[idx] > 0:
                disappeared_numbers.append(val)

        # Overall Time Complexity: O(n) - Two passes through the array
        # Overall Space Complexity: O(1) - Only modifying input array in-place (output list not counted)
        return disappeared_numbers


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_case_1(self):
        # Standard case
        self.assertEqual(self.sol.find_disappeared_numbers([4, 3, 2, 7, 8, 2, 3, 1]), [5, 6])

    def test_case_2(self):
        # Small case with one missing
        self.assertEqual(self.sol.find_disappeared_numbers([1, 1]), [2])

    def test_case_3(self):
        # All numbers present
        self.assertEqual(self.sol.find_disappeared_numbers([1, 2, 3]), [])

    def test_case_4(self):
        # All numbers missing except one
        self.assertEqual(self.sol.find_disappeared_numbers([1, 1, 1]), [2, 3])

    def test_case_5(self):
        # Empty input (though n >= 1 usually)
        self.assertEqual(self.sol.find_disappeared_numbers([]), [])


if __name__ == "__main__":
    unittest.main()
