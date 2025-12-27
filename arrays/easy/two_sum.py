import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY)
------------------------------------------
1. Dict for O(1) Lookups: Using a dictionary (hash map) allows you to check
   for the existence of a 'complement' in constant time, turning an O(n^2)
   problem into O(n).
2. enumerate(): Use `for i, num in enumerate(nums):` to keep track of both
   the value and its index simultaneously without manual counters.
3. Membership Testing: `if key in dict:` is O(1) on average. Avoid 
   `if val in list:`, which is O(n) and can lead to accidental O(n^2) logic.
4. Type Hinting: Always use `list[int]` or `dict[int, int]` to show you are
   comfortable with modern Python (3.9+) standards.
"""


class Solution:
    def two_sum(self, nums: list[int], target: int) -> list[int]:
        """
        PROBLEM: TWO SUM
        Given an array of integers 'nums' and an integer 'target', return
        indices of the two numbers such that they add up to 'target'.

        REQUIREMENTS:
        - Each input has exactly one solution.
        - You may not use the same element twice.
        - You can return the answer in any order.
        - Aim for O(n) time complexity.

        :param nums: A list of integers.
        :param target: The integer sum to find.
        :return: A list containing the two indices.
        """
        # Space: O(n) - stores up to n elements
        number_by_index: dict[int, int] = {}

        # Time: O(n) - single pass through array
        for idx, val in enumerate(nums):  
            complement = target - val  
            if complement in number_by_index:  
                return [number_by_index[complement], idx]
            number_by_index[val] = idx

        # Overall Time Complexity: O(n) - single pass through the array
        # Overall Space Complexity: O(n) - dictionary stores at most n elements
        return [] 


class TestTwoSum(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard(self):
        self.assertEqual(sorted(self.sol.two_sum([2, 7, 11, 15], 9)), [0, 1])

    def test_non_consecutive(self):
        self.assertEqual(sorted(self.sol.two_sum([3, 2, 4], 6)), [1, 2])

    def test_same_values(self):
        # Testing that we don't use the same element twice
        self.assertEqual(sorted(self.sol.two_sum([3, 3], 6)), [0, 1])

    def test_negative_numbers(self):
        self.assertEqual(sorted(self.sol.two_sum([-1, -2, -3, -4, -5], -8)), [2, 4])

    def test_large_target(self):
        self.assertEqual(sorted(self.sol.two_sum([10, 20, 30, 40, 50, 75], 125)), [4, 5])


if __name__ == "__main__":
    unittest.main()
