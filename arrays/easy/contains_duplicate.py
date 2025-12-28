import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY - HASH SETS)
-------------------------------------------------------
1. set(): A collection of unique elements. Lookups (`if x in my_set`) 
   and insertions (`my_set.add(x)`) are O(1) on average.
2. len(set(nums)) < len(nums): A classic "Pythonic" trick to check for 
   duplicates in one line. It compares the size of the unique elements 
   to the size of the original list.
3. Early Exit: In many "Exists" problems, you should return True the 
   moment you find a match to save time in the average case.
4. Sorting Trade-off: Sorting a list takes O(n log n) time but uses 
   O(1) extra space. Using a set takes O(n) time but O(n) space.
"""


class Solution:
    def contains_duplicate(self, nums: list[int]) -> bool:
        """
        PROBLEM: CONTAINS DUPLICATE
        Given an integer array 'nums', return True if any value appears
        at least twice in the array, and return False if every element
        is distinct.

        REQUIREMENTS:
        - Aim for O(n) time complexity.
        - Think about how to use extra space to speed up the lookup.

        :param nums: A list of integers.
        :return: Boolean (True if duplicates exist).
        """
        # Space: O(n) to store up to n unique elements
        already_in: set[int] = set()

        # Time: O(n) to iterate through all elements
        for val in nums:
            # Time: O(1) average case for set membership check
            if val in already_in:
                return True
            # Time: O(1) average case for set insertion
            already_in.add(val)

        return False


class TestContainsDuplicate(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_has_duplicate(self):
        self.assertTrue(self.sol.contains_duplicate([1, 2, 3, 1]))

    def test_all_distinct(self):
        self.assertFalse(self.sol.contains_duplicate([1, 2, 3, 4]))

    def test_multiple_duplicates(self):
        self.assertTrue(self.sol.contains_duplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]))

    def test_empty_list(self):
        self.assertFalse(self.sol.contains_duplicate([]))

    def test_single_element(self):
        self.assertFalse(self.sol.contains_duplicate([1]))


if __name__ == "__main__":
    unittest.main()
