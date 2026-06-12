import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY)  
------------------------------------------  
1. collections.Counter: A dict subclass for counting hashable objects. 
   Extremely efficient for frequency maps. Counter(nums) builds the map in O(n).
2. Dictionary .get() method: dict.get(key, 0) allows you to access a value 
   without checking 'if key in dict' first, preventing KeyErrors.
3. List Comprehension: While loops are fine, list comprehensions or 
   generator expressions are often more idiomatic for small-scale filtering.
4. Memory Efficiency: In Python, modifying a list in-place (if possible) 
   saves space, though for intersection, returning a new list is standard.
"""


class Solution:
    def intersection_two_arrays(self, nums1: List[int], nums2: List[int]) -> List[int]:
        """
        PROBLEM: INTERSECTION OF TWO ARRAYS II
        Given two integer arrays nums1 and nums2, return an array of their intersection.
        Each element in the result must appear as many times as it shows in both arrays
        and you may return the result in any order.

        REQUIREMENTS:
        - Return a list containing common elements with correct frequencies.
        - Handle duplicate values correctly.
        - Time Complexity must be O(n + m).
        - Space Complexity must be O(min(n, m)).

        :param nums1: First list of integers.
        :param nums2: Second list of integers.
        :return: List of common elements.
        """
        repeats: dict[int, int] = dict()

        shortest = nums1 if len(nums1) < len(nums2) else nums2
        longest = nums1 if len(nums1) >= len(nums2) else nums2

        for val in shortest:  # Time: O(min(n, m)), Space: O(min(n, m)) - Iterate through shorter array, dict grows up to min(n, m) unique elements
            if val not in repeats:
                repeats[val] = 0
            repeats[val] += 1

        intersection: list[int] = list()

        for val in longest:  # Time: O(max(n, m)), Space: O(min(n, m)) worst case - Iterate through longer array, result list grows up to min(n, m) elements
            if val in repeats:
                intersection.append(val)
                repeats[val] -= 1
                if repeats[val] == 0:
                    del repeats[val]

        return intersection

        # Time: O(n + m) where n = len(nums1) and m = len(nums2)
        # Space: O(min(n, m))


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_case_1(self):
        # Basic overlap
        self.assertEqual(sorted(self.sol.intersection_two_arrays([1, 2, 2, 1], [2, 2])), [2, 2])

    def test_case_2(self):
        # Multiple different overlapping elements
        result = sorted(self.sol.intersection_two_arrays([4, 9, 5], [9, 4, 9, 8, 4]))
        self.assertEqual(result, [4, 9])

    def test_case_3(self):
        # No intersection
        self.assertEqual(self.sol.intersection_two_arrays([1, 2, 3], [4, 5, 6]), [])

    def test_case_4(self):
        # One array is empty
        self.assertEqual(self.sol.intersection_two_arrays([], [1, 1]), [])

    def test_case_5(self):
        # All elements are the same
        self.assertEqual(sorted(self.sol.intersection_two_arrays([1, 1], [1, 1])), [1, 1])


if __name__ == "__main__":
    unittest.main()
