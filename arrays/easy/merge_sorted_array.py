import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY - BACKWARDS MERGE)
------------------------------------------------------------
1. Reverse Iteration: Using `range(start, stop, step)` with a step of -1 
   is common for "backwards" problems. E.g., `range(m + n - 1, -1, -1)`.
2. In-Place Constraints: When a problem says "do not return anything, 
   modify nums1 in-place," it means any changes must happen to the 
   original object passed into the function.
3. Pointer Logic: Using multiple variables (i, j, k) to track different 
   positions in arrays is the bread and butter of array optimization.
4. While Loops vs For Loops: While loops are often cleaner for 
   multi-pointer problems where you don't know exactly how many steps 
   each pointer will take.
"""


class Solution:
    def merge_sorted_array(self, nums1: list[int], m: int, nums2: list[int], n: int) -> None:
        """
        PROBLEM: MERGE SORTED ARRAY
        You are given two integer arrays 'nums1' and 'nums2', sorted in
        non-decreasing order, and two integers 'm' and 'n', representing
        the number of elements in nums1 and nums2 respectively.

        'nums1' has a total length of m + n, where the first m elements
        denote the elements that should be merged, and the last n elements
        are set to 0 and should be ignored. nums2 has a length of n.

        REQUIREMENTS:
        - Merge nums2 into nums1 as a single sorted array IN-PLACE.
        - Do not return anything.
        - Aim for O(m + n) time complexity.

        :param nums1: List of m + n integers (m active, n padding).
        :param m: Number of active elements in nums1.
        :param nums2: List of n integers.
        :param n: Number of elements in nums2.
        """
        n1_idx = m - 1
        n2_idx = n - 1
        final_idx = (m + n) - 1

        # Time: O(m + n) - iterate through all elements from both arrays once
        # Space: O(1) - only using constant extra space for pointers
        while n1_idx >= 0 and n2_idx >= 0:
            if nums1[n1_idx] > nums2[n2_idx]:
                nums1[final_idx] = nums1[n1_idx]
                n1_idx -= 1
            else:
                nums1[final_idx] = nums2[n2_idx]
                n2_idx -= 1
            final_idx -= 1

        # Time: O(n) worst case - copy remaining elements from nums2
        # Space: O(1) - only using constant extra space for pointers
        while n2_idx >= 0:
            nums1[final_idx] = nums2[n2_idx]
            n2_idx -= 1
            final_idx -= 1


class TestMergeSortedArray(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_merge(self):
        n1, n2 = [1, 2, 3, 0, 0, 0], [2, 5, 6]
        self.sol.merge_sorted_array(n1, 3, n2, 3)
        self.assertEqual(n1, [1, 2, 2, 3, 5, 6])

    def test_single_element_n1(self):
        n1, n2 = [1], []
        self.sol.merge_sorted_array(n1, 1, n2, 0)
        self.assertEqual(n1, [1])

    def test_single_element_n2(self):
        n1, n2 = [0], [1]
        self.sol.merge_sorted_array(n1, 0, n2, 1)
        self.assertEqual(n1, [1])

    def test_n2_all_smaller(self):
        n1, n2 = [4, 5, 6, 0, 0, 0], [1, 2, 3]
        self.sol.merge_sorted_array(n1, 3, n2, 3)
        self.assertEqual(n1, [1, 2, 3, 4, 5, 6])

    def test_n2_all_larger(self):
        n1, n2 = [1, 2, 3, 0, 0, 0], [4, 5, 6]
        self.sol.merge_sorted_array(n1, 3, n2, 3)
        self.assertEqual(n1, [1, 2, 3, 4, 5, 6])


if __name__ == "__main__":
    unittest.main()
