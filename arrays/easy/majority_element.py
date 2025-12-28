import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: FREQUENCY TRACKING (EASY)  
------------------------------------------  
1. collections.Counter: A specialized dictionary for counting hashable 
   objects. `Counter(nums).most_common(1)` is a very Pythonic way to 
   solve this, though interviewers may want to see the manual logic.
2. dict.get(key, default): Safely access a dictionary key. 
   `counts[n] = counts.get(n, 0) + 1` is cleaner than `if n in counts`.
3. Boyer-Moore Voting Algorithm: A brilliant $O(n)$ time and $O(1)$ space 
   algorithm designed specifically to find the majority element.
4. Sorting: Sorting the array and returning `nums[n // 2]` always works 
   for a majority element but costs $O(n \log n)$ time.
"""


class Solution:
    def majority_element(self, nums: List[int]) -> int:
        """
        PROBLEM: MAJORITY ELEMENT
        Given an array `nums` of size `n`, return the majority element.
        The majority element is the element that appears more than
        ⌊n / 2⌋ times. You may assume that the majority element
        always exists in the array.

        REQUIREMENTS:
        - Return the integer value of the majority element.
        - Time Complexity must be $O(n)$.
        - Space Complexity should aim for $O(1)$ (if using Boyer-Moore).

        :param nums: A list of integers.
        :return: The majority element.
        """
        counter = 1
        element = nums[0]

        for val in nums[1:]:  # O(n) time | O(1) space - Iterate through remaining elements
            if val == element:
                counter += 1
            else:
                counter -= 1

            if counter == 0:
                counter = 1
                element = val

        return element


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_case(self):
        # 3 appears twice, 2 appears once. 2 > 3/2.
        self.assertEqual(self.sol.majority_element([3, 2, 3]), 3)

    def test_clear_majority(self):
        # 2 appears four times in a list of seven.
        self.assertEqual(self.sol.majority_element([2, 2, 1, 1, 1, 2, 2]), 2)

    def test_single_element(self):
        self.assertEqual(self.sol.majority_element([1]), 1)

    def test_two_elements(self):
        # Both same, so either is majority
        self.assertEqual(self.sol.majority_element([5, 5]), 5)

    def test_large_numbers(self):
        self.assertEqual(self.sol.majority_element([1000000, 1000000, 1]), 1000000)


if __name__ == "__main__":
    unittest.main()
