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
    def move_zeroes(self, nums: list[int]) -> None:
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
        if len(nums) < 2:
            return nums

        placement = 0  # Keeps the placement for discovered non-zero

        for val in nums:
            if val != 0:
                nums[placement] = val
                placement += 1

        nums[placement:] = [0] * (len(nums) - placement)

        return nums


class TestMoveZeroes(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_case(self):
        tc1 = [0, 1, 0, 3, 12]
        self.sol.move_zeroes(tc1)
        self.assertEqual(tc1, [1, 3, 12, 0, 0])

    def test_no_zeroes(self):
        tc2 = [1, 2, 3]
        self.sol.move_zeroes(tc2)
        self.assertEqual(tc2, [1, 2, 3])

    def test_all_zeroes(self):
        tc3 = [0, 0, 0]
        self.sol.move_zeroes(tc3)
        self.assertEqual(tc3, [0, 0, 0])

    def test_single_zero(self):
        tc4 = [0]
        self.sol.move_zeroes(tc4)
        self.assertEqual(tc4, [0])

    def test_zero_at_the_end(self):
        tc5 = [1, 0]
        self.sol.move_zeroes(tc5)
        self.assertEqual(tc5, [1, 0])


if __name__ == "__main__":
    unittest.main()
