import unittest
from typing import List

"""  
PYTHON INTERVIEW CHEAT-SHEET: NESTED ARRAYS (EASY)  
------------------------------------------  
1. List Initialization: `[1] * n` creates a list of size n filled with 1s.
2. Indexing Boundaries: When accessing `j-1` or `j+1`, always ensure 
   your loop range starts/ends to avoid `IndexError`.
3. List of Lists: Appending a list to another list `res.append(row)` 
   is $O(1)$ because you are appending a reference.
4. Symmetry: Remember that Pascal's Triangle is symmetric; while not 
   required for the solution, it's a great observation to mention.
"""


class Solution:
    def pascal_triangle(self, numRows: int) -> List[List[int]]:
        """
        PROBLEM: PASCAL'S TRIANGLE
        Given an integer `numRows`, return the first `numRows` of
        Pascal's triangle.

        In Pascal's triangle, each number is the sum of the two
        numbers directly above it.

        REQUIREMENTS:
        - Return a list of lists of integers.
        - Time Complexity must be $O(numRows^2)$.
        - Space Complexity must be $O(numRows^2)$ for the output.

        :param numRows: The number of rows to generate.
        :return: Pascal's triangle as a list of lists.
        """
        triangle: list[list[int]] = [[1]]
        if numRows == 1:
            return triangle

        for lvl in range(1, numRows):  # O(numRows) - iterate through each level
            parent = triangle[lvl - 1]
            new_lvl = [parent[0]]
            for right_idx in range(1, len(parent)):  # O(lvl) - iterate through parent elements
                new_lvl.append(parent[right_idx - 1] + parent[right_idx])

            new_lvl.append(parent[-1])
            triangle.append(new_lvl)

        return triangle

        # Time Complexity: O(numRows^2) - We iterate through numRows levels, and for each level i, we perform i operations
        # Space Complexity: O(numRows^2) - We store all elements of the triangle, which totals 1+2+3+...+numRows = numRows*(numRows+1)/2 elements


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_five_rows(self):
        expected = [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
        self.assertEqual(self.sol.pascal_triangle(5), expected)

    def test_one_row(self):
        self.assertEqual(self.sol.pascal_triangle(1), [[1]])

    def test_two_rows(self):
        self.assertEqual(self.sol.pascal_triangle(2), [[1], [1, 1]])


if __name__ == "__main__":
    unittest.main()
