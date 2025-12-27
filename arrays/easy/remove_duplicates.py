import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY - TWO POINTERS)
---------------------------------------------------------
1. In-Place Modification: When asked to modify a list in-place, you are 
   overwriting values at existing indices rather than using `.append()` 
   or creating a new list.
2. Two-Pointer Technique: Use one 'slow' pointer to track the position of 
   the last unique element and a 'fast' pointer to scan the array.
3. f-strings: Great for debugging. `print(f"Index {i} has value {nums[i]}")`.
4. del or slicing: To actually resize a list in-place in Python, you can 
   use `nums[:] = nums[:k]`, though many interviewers only care about the 
   first k elements being correct.
"""


class Solution:
    def remove_duplicates(self, nums: list[int]) -> int:
        """
        PROBLEM: REMOVE DUPLICATES FROM SORTED ARRAY
        Given an integer array 'nums' sorted in non-decreasing order, remove
        the duplicates IN-PLACE such that each unique element appears only once.
        The relative order of the elements should be kept the same.

        Then return the number of unique elements in 'nums'.

        REQUIREMENTS:
        - Modify the input array 'nums' in-place.
        - Space Complexity: O(1).
        - Time Complexity: O(n).

        :param nums: A list of integers sorted in ascending order.
        :return: The number of unique elements (k).
        """
        # Time: O(1) - Edge case check
        if not nums:
            return 0

        # 'last_unique_index' is the index of the last unique element found
        # Space: O(1) - Single pointer variable
        last_unique_index = 0

        # 'current_index' scans through the array
        # Time: O(n) - Single pass through array
        for current_index in range(1, len(nums)):
            # If we find a new unique value
            # Time: O(1) - Constant time comparison
            if nums[current_index] != nums[last_unique_index]:
                # Time: O(1) - Constant time operations
                last_unique_index += 1
                nums[last_unique_index] = nums[current_index]  # Overwrite in-place

        # k is the count of unique elements
        # Space: O(1) - Single variable
        k = last_unique_index + 1

        # Optional: True in-place resize for Pythonic completeness
        # Time: O(n + k) > O(k) - Original n deletes + Slice assignment copies k elements; Space: O(1) - In-place modification
        # nums[:] = nums[:k]

        # Time: O(1) - Return operation
        return k


class TestRemoveDuplicates(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard(self):
        nums = [1, 1, 2]
        k = self.sol.remove_duplicates(nums)
        self.assertEqual(k, 2)
        self.assertEqual(nums[:k], [1, 2])

    def test_longer_array(self):
        nums = [0, 0, 1, 1, 1, 2, 2, 3, 3, 4]
        k = self.sol.remove_duplicates(nums)
        self.assertEqual(k, 5)
        self.assertEqual(nums[:k], [0, 1, 2, 3, 4])

    def test_no_duplicates(self):
        nums = [1, 2, 3]
        k = self.sol.remove_duplicates(nums)
        self.assertEqual(k, 3)
        self.assertEqual(nums[:k], [1, 2, 3])

    def test_empty(self):
        nums = []
        k = self.sol.remove_duplicates(nums)
        self.assertEqual(k, 0)

    def test_all_same(self):
        nums = [1, 1, 1, 1]
        k = self.sol.remove_duplicates(nums)
        self.assertEqual(k, 1)
        self.assertEqual(nums[:k], [1])


if __name__ == "__main__":
    unittest.main()
