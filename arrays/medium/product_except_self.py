import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (MEDIUM - PREFIX/SUFFIX)
------------------------------------------------------------
1. Space Optimization: Often, you can use the 'result' array to store
   intermediate prefix products and then update it in-place with suffix
   products to achieve O(1) extra space.
2. Avoiding Division: Interviews often restrict the use of the `/` operator.
   This forces you to think about how to build a value from its components.
3. List Initialization: `res = [1] * len(nums)` is a fast, Pythonic way
   to prepare an array for multiplicative identity operations.
4. Range Step -1: `range(n - 1, -1, -1)` is how you iterate backwards 
   through an array in Python—essential for suffix/reverse passes.
"""


class Solution:
    def product_except_self(self, nums: list[int]) -> list[int]:
        """
        PROBLEM: PRODUCT OF ARRAY EXCEPT SELF
        Given an integer array 'nums', return an array 'answer' such that
        answer[i] is equal to the product of all the elements of nums
        except nums[i].

        REQUIREMENTS:
        - The algorithm MUST run in O(n) time.
        - You MUST NOT use the division operation.
        - You should aim to solve it using O(1) extra space complexity
          (the output array does not count as extra space).

        :param nums: A list of integers.
        :return: A list of integers representing the products.
        """
        n = len(nums)
        res = [1] * n

        # Pass 1: Prefix Products
        # Calculate the product of all elements to the LEFT of i
        # For each index i, res[i] stores the cumulative product of all elements
        # before index i (nums[0] * nums[1] * ... * nums[i-1]).
        # The 'prefix' variable acts as a running product that accumulates values
        # as we iterate left-to-right. Initially, res[0] = 1 (no elements to its left),
        # then res[1] = nums[0], res[2] = nums[0] * nums[1], and so on.
        # Time: O(n), Space: O(1) excluding output array
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]

        # Pass 2: Suffix Products
        # Calculate the product of all elements to the RIGHT of i
        # and multiply it by the existing prefix product in res[i]
        # For each index i (traversing right-to-left), res[i] currently holds the prefix
        # product (all elements to the left of i). We now multiply it by the 'suffix' variable,
        # which represents the cumulative product of all elements to the right of i.
        # The 'suffix' variable starts at 1 (no elements to the right of the last index),
        # then as we move left, suffix accumulates: nums[n-1], nums[n-1]*nums[n-2], etc.
        # After this pass, res[i] = nums[0]*...*nums[i-1] * nums[i+1]*...*nums[n-1].
        # Time: O(n), Space: O(1) excluding output array
        suffix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= suffix
            suffix *= nums[i]

        # Overall Time Complexity: O(n), Space Complexity: O(1)
        return res


class TestProductExceptSelf(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_case(self):
        # Result: [2*3*4, 1*3*4, 1*2*4, 1*2*3] = [24, 12, 8, 6]
        self.assertEqual(self.sol.product_except_self([1, 2, 3, 4]), [24, 12, 8, 6])

    def test_with_negatives(self):
        self.assertEqual(self.sol.product_except_self([-1, 1, 0, -3, 3]), [0, 0, 9, 0, 0])

    def test_all_zeros(self):
        self.assertEqual(self.sol.product_except_self([0, 0, 0]), [0, 0, 0])

    def test_two_elements(self):
        self.assertEqual(self.sol.product_except_self([10, 20]), [20, 10])

    def test_large_numbers(self):
        self.assertEqual(self.sol.product_except_self([1, 5, 2, 3]), [30, 6, 15, 10])


if __name__ == "__main__":
    unittest.main()
