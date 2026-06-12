import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY)  
------------------------------------------  
1. In-place Mutation: When a problem asks for O(1) space, look for 
   "Two-Pointer" solutions where one pointer tracks the 'write' position.
2. list.pop() vs. Swapping: Removing an element via pop(i) is O(n) because 
   elements must shift. Swapping or overwriting via pointers is O(1).
3. Under-the-hood: Python lists are dynamic arrays. Overwriting values 
   at indices is significantly faster than resizing the list.
4. Slicing: remember that `nums[:] = ...` modifies the original list 
   object in-place, whereas `nums = ...` only rebinds the local name.
"""


class Solution:
    def remove_element(self, nums: List[int], val: int) -> int:
        """
        PROBLEM: REMOVE ELEMENT
        Given an integer array nums and an integer val, remove all occurrences
        of val in nums in-place. The order of the elements may be changed.
        Then return the number of elements in nums which are not equal to val.

        Consider the number of elements in nums which are not equal to val be k,
        to get accepted, you need to do the following things:
        1. Modify the array nums such that the first k elements of nums contain
           the elements which are not equal to val.
        2. Return k.

        REQUIREMENTS:
        - Modify 'nums' in-place.
        - Return the count of elements not equal to 'val'.
        - Time Complexity must be O(n).
        - Space Complexity must be O(1).

        :param nums: List of integers.
        :param val: The integer to remove.
        :return: Number of elements remaining.
        """
        slow_idx = 0

        for can in nums:  # Time: O(n) - iterate through all n elements once
            if can != val:
                nums[slow_idx] = can
                slow_idx += 1

        return slow_idx

        # Overall Time Complexity: O(n), Space Complexity: O(1)


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_case_1(self):
        nums = [3, 2, 2, 3]
        val = 3
        k = self.sol.remove_element(nums, val)
        self.assertEqual(k, 2)
        self.assertEqual(sorted(nums[:k]), [2, 2])

    def test_case_2(self):
        nums = [0, 1, 2, 2, 3, 0, 4, 2]
        val = 2
        k = self.sol.remove_element(nums, val)
        self.assertEqual(k, 5)
        self.assertEqual(sorted(nums[:k]), [0, 0, 1, 3, 4])

    def test_case_3(self):
        # All elements match val
        nums = [1, 1, 1]
        val = 1
        k = self.sol.remove_element(nums, val)
        self.assertEqual(k, 0)

    def test_case_4(self):
        # No elements match val
        nums = [1, 2, 3]
        val = 4
        k = self.sol.remove_element(nums, val)
        self.assertEqual(k, 3)
        self.assertEqual(sorted(nums[:k]), [1, 2, 3])

    def test_case_5(self):
        # Empty array
        nums = []
        val = 0
        k = self.sol.remove_element(nums, val)
        self.assertEqual(k, 0)


if __name__ == "__main__":
    unittest.main()
