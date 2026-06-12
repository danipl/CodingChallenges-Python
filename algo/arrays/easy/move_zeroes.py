import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (LOW)
------------------------------------------
1. List Slicing: `arr[::-1]` reverses a list in O(n), while `arr[a:b]`
   creates a shallow copy. Useful for sub-segment problems.
2. enumerate(): Always use `for i, val in enumerate(nums):` instead of
   `range(len(nums))` when you need both index and value. It's more Pythonic.
3. In-place Updates: To keep Space Complexity at O(1), try to modify the
   input list directly rather than creating a new one.
4. List Comprehensions: `[x for x in nums if x > 0]` is faster and more
   readable than manual loops for filtering.
"""


class Solution:
    def move_zeroes(self, nums: list[int]):
        """
        PROBLEM: MOVE ZEROES
        Given an integer array 'nums', move all 0's to the end of it while
        maintaining the relative order of the non-zero elements.

        REQUIREMENTS:
        - You must do this IN-PLACE without making a copy of the array.
        - Minimize the total number of operations.

        :param nums: A list of integers.
        :return: None (Modify nums in-place).
        """
        # Time: O(1) - early return for edge case
        if len(nums) < 2:
            return

        placement = 0

        # Time: O(n) - single pass through array
        # Space: O(1) - only using a pointer variable
        for val in nums:
            if val != 0:
                nums[placement] = val
                placement += 1

        # Original: nums[placement:] = [0] * (len(nums) - placement)
        # To avoid O(n) space complexity from list slicing, fill zeros manually
        # Time: O(n) - worst case fills entire array with zeros
        # Space: O(1) - in-place modification
        for i in range(placement, len(nums)):
            nums[i] = 0


class TestMoveZeroes(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_case(self):
        tc1 = [0, 1, 0, 3, 12]
        self.sol.move_zeroes(tc1)
        self.assertEqual(tc1, [1, 3, 12, 0, 0])

    def test_alternating_zeros_and_numbers(self):
        tc2 = [0, 1, 0, 2, 0, 3, 0, 4]
        self.sol.move_zeroes(tc2)
        self.assertEqual(tc2, [1, 2, 3, 4, 0, 0, 0, 0])

    def test_multiple_consecutive_zeros(self):
        tc3 = [1, 0, 0, 0, 2, 0, 0, 3]
        self.sol.move_zeroes(tc3)
        self.assertEqual(tc3, [1, 2, 3, 0, 0, 0, 0, 0])

    def test_large_array(self):
        tc4 = [0, 5, 0, 0, 10, 15, 0, 20, 0, 25, 30, 0, 0, 35]
        self.sol.move_zeroes(tc4)
        self.assertEqual(tc4, [5, 10, 15, 20, 25, 30, 35, 0, 0, 0, 0, 0, 0, 0])

    def test_negative_numbers(self):
        tc5 = [0, -1, 0, -2, 3, 0, -4]
        self.sol.move_zeroes(tc5)
        self.assertEqual(tc5, [-1, -2, 3, -4, 0, 0, 0])

    def test_single_nonzero(self):
        tc6 = [5, 0, 0, 0]
        self.sol.move_zeroes(tc6)
        self.assertEqual(tc6, [5, 0, 0, 0])

    def test_no_zeroes(self):
        tc7 = [1, 2, 3]
        self.sol.move_zeroes(tc7)
        self.assertEqual(tc7, [1, 2, 3])

    def test_all_zeroes(self):
        tc8 = [0, 0, 0]
        self.sol.move_zeroes(tc8)
        self.assertEqual(tc8, [0, 0, 0])

    def test_single_zero(self):
        tc9 = [0]
        self.sol.move_zeroes(tc9)
        self.assertEqual(tc9, [0])

    def test_zero_at_the_end(self):
        tc10 = [1, 0]
        self.sol.move_zeroes(tc10)
        self.assertEqual(tc10, [1, 0])


if __name__ == "__main__":
    unittest.main()
