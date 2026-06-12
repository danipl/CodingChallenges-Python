import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY - MATH/LOGIC)
--------------------------------------------------------
1. Modulo & Integer Division: `digit % 10` gives the remainder (the new digit),
   while `digit // 10` gives the carry.
2. In-Place vs. New List: Most array math problems prefer in-place updates,
   but if the length changes (e.g., 99 + 1 = 100), you must return a new list.
3. [1] + digits: In Python, you can easily prepend an element to a list 
   using the `+` operator. It creates a new list in O(n) time.
4. Reversed Traversal: For math problems (addition, multiplication), 
   always start from the end: `range(len(digits) - 1, -1, -1)`.
"""


class Solution:
    def plus_one(self, digits: list[int]) -> list[int]:
        """
        PROBLEM: PLUS ONE
        You are given a large integer represented as an integer array 'digits',
        where each digits[i] is the i-th digit of the integer. The digits
        are ordered from most significant to least significant in left-to-right
        order. The large integer does not contain any leading 0's.

        Increment the large integer by one and return the resulting array of digits.

        REQUIREMENTS:
        - Time Complexity: O(n)
        - Space Complexity: O(1) (excluding the space for the result)

        :param digits: A list of integers (0-9).
        :return: A list of integers representing the incremented value.
        """
        if not digits:
            return digits

        # Time: O(n) in worst case (all 9s), O(1) average case (first digit < 9)
        for i in range(len(digits) - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits

            digits[i] = 0

        # Space: O(n) - creates new list with n+1 elements
        return [1] + digits

        # Overall Time Complexity: O(n) - may traverse entire array in worst case
        # Overall Space Complexity: O(1) - in-place modification, except O(n) when creating new list for all-9s case


class TestPlusOne(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard(self):
        self.assertEqual(self.sol.plus_one([1, 2, 3]), [1, 2, 4])

    def test_carry_single(self):
        self.assertEqual(self.sol.plus_one([1, 2, 9]), [1, 3, 0])

    def test_all_nines(self):
        # The ultimate boundary case: number of digits increases
        self.assertEqual(self.sol.plus_one([9, 9, 9]), [1, 0, 0, 0])

    def test_single_digit_not_nine(self):
        self.assertEqual(self.sol.plus_one([4]), [5])

    def test_single_digit_nine(self):
        self.assertEqual(self.sol.plus_one([9]), [1, 0])


if __name__ == "__main__":
    unittest.main()
