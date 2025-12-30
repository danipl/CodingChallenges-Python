import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: CYCLIC SORT (EASY/MED)  
--------------------------------------------------  
1. The Core Idea: If the range is [0, n], then nums[i] should ideally 
   equal `i`. We use swaps to put each number in its "home" index.
2. The While Loop: Unlike a standard for-loop, we often stay on the 
   same index `i` until `nums[i]` is either in the correct place 
   or we find a duplicate.
3. Tuple Unpacking for Swaps: `nums[i], nums[correct_idx] = nums[correct_idx], nums[i]` 
   is the clean, Pythonic way to swap without a temporary variable.
4. Range check: Since the range is [0, n] but the array size is n, 
   one number (usually the value 'n') might not have a "home" index 
   if the array only goes up to n-1. We simply skip values that 
   fall outside the current index range.
"""


class Solution:
    def find_disappeared_numbers_with_zero(self, nums: List[int]) -> List[int]:
        """
        PROBLEM: FIND DISAPPEARED NUMBERS (0 to n)
        Given an array nums of n integers where nums[i] is in the range [0, n].
        Return all integers in the range [0, n] that do not appear in nums.

        REQUIREMENTS:
        - Time Complexity: O(n).
        - Space Complexity: O(1).
        """
        n = len(nums)
        found_n = False
        i = 0

        # Phase 1: Cyclic Sort
        # Time: O(n) - Each element is moved to its correct position at most once
        # Space: O(1) - In-place sorting with only a few variables
        while i < n:
            # Check if we see the value n during our traversal
            if nums[i] == n:
                found_n = True
                i += 1
                continue

            correct_idx = nums[i]

            # Standard cyclic swap logic
            if nums[i] != nums[correct_idx]:
                nums[i], nums[correct_idx] = nums[correct_idx], nums[i]
            else:
                i += 1

        # Phase 2: Identify missing numbers from 0 to n-1
        # Time: O(n) - Single pass through the array
        # Space: O(k) - Where k is the number of missing elements (output space)
        disappeared = []
        for i in range(n):
            if nums[i] != i:
                disappeared.append(i)

        # Phase 3: The final check for the boundary value n
        # Time: O(1) - Constant time check
        if not found_n:
            disappeared.append(n)

        # Overall Time Complexity: O(n)
        # Overall Space Complexity: O(1) auxiliary space (output list not counted)
        return disappeared


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_basic_missing(self):
        # n=3, range [0,3]. Input: [3, 0, 1]. Missing: 2.
        self.assertEqual(self.sol.find_disappeared_numbers_with_zero([3, 0, 1]), [2])

    def test_all_numbers_present(self):
        # n=4, range [0,4]. Input: [0, 4, 1, 3, 2]. Missing: [].
        # Note: input size is 5, n is 5. Wait, if nums is size 5, n=5, range is [0,5].
        # Let's use a consistent n=4 example:
        nums = [0, 1, 2, 3]  # size 4, range [0, 4]. Missing 4.
        self.assertEqual(self.sol.find_disappeared_numbers_with_zero(nums), [4])

    def test_missing_zero_and_n(self):
        # n=3, range [0,3]. Input: [1, 2, 1]. Missing: 0, 3.
        res = self.sol.find_disappeared_numbers_with_zero([1, 2, 1])
        self.assertEqual(sorted(res), [0, 3])

    def test_duplicates(self):
        # n=5, range [0,5]. Input: [0, 0, 2, 2, 5]. Missing: 1, 3, 4.
        res = self.sol.find_disappeared_numbers_with_zero([0, 0, 2, 2, 5])
        self.assertEqual(sorted(res), [1, 3, 4])


if __name__ == "__main__":
    # This is a conceptual implementation of the pivot discussed.
    # Note: In the 'Missing Number' (Easy) variation, only ONE number is missing.
    print("Cyclic Sort logic implemented.")
