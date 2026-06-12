import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS & GREEDY (EASY)  
--------------------------------------------------  
1. Greedy Approach: In this problem, planting a flower as soon as you find 
   a valid spot is optimal because it never hinders future possibilities 
   more than waiting would.
2. Boundary Padding: To avoid complex "if index == 0" or "if index == len-1" 
   checks, you can temporarily pad the array: `f = [0] + flowerbed + [0]`.
3. Early Exit: If the number of flowers to plant `n` reaches 0, you can 
   return True immediately to save time.
4. Range Logic: Remember that `range(len(flowerbed))` is standard, but if 
   you pad the array, adjust your loop boundaries accordingly.
"""


class Solution:
    def can_place_flowers(self, flowerbed: List[int], n: int) -> bool:
        """
        PROBLEM: CAN PLACE FLOWERS
        You have a flowerbed represented by an array of 0s and 1s.
        Flowers cannot be planted in adjacent plots (no two 1s can be next to each other).

        Given 'flowerbed' and an integer 'n', return True if 'n' flowers can be
        planted, False otherwise.

        REQUIREMENTS:
        - Time Complexity: O(length of flowerbed).
        - Space Complexity: O(1) or O(length of flowerbed) if padding is used.
        - Handle edge cases: Single plot beds, planting 0 flowers, etc.

        :param flowerbed: List of 0s and 1s.
        :param n: Number of flowers to plant.
        :return: Boolean.
        """
        if not flowerbed:
            return False
        elif n == 0:
            return True

        planted = 0

        # Time: O(n), Space: O(1) - single pass through array
        for idx, val in enumerate(flowerbed):
            left = flowerbed[idx - 1] if idx > 0 else 0
            right = flowerbed[idx + 1] if idx < len(flowerbed) - 1 else 0

            if left == 0 and val == 0 and right == 0:
                flowerbed[idx] = 1
                planted += 1

        return planted >= n


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_case_1(self):
        # Normal valid case
        self.assertTrue(self.sol.can_place_flowers([1, 0, 0, 0, 1], 1))

    def test_case_2(self):
        # Normal invalid case (adjacent)
        self.assertFalse(self.sol.can_place_flowers([1, 0, 0, 0, 1], 2))

    def test_case_3(self):
        # Empty bed, multiple spots
        self.assertTrue(self.sol.can_place_flowers([0, 0, 0, 0, 0], 3))

    def test_case_4(self):
        # Single element bed
        self.assertTrue(self.sol.can_place_flowers([0], 1))
        self.assertFalse(self.sol.can_place_flowers([1], 1))

    def test_case_5(self):
        # Planting 0 flowers is always True
        self.assertTrue(self.sol.can_place_flowers([1, 1, 1], 0))


if __name__ == "__main__":
    unittest.main()
