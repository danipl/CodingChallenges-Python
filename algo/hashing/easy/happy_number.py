import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: HASHING (EASY)
------------------------------------------
1. set() for O(1) Membership Testing: `if val in my_set` is O(1) average.
   Use this to track visited states and detect cycles instantly.
2. Cycle Detection Pattern: If you're following a sequence and need to know
   if it loops, store each seen value in a set. A duplicate = cycle.
3. Divmod: `quotient, remainder = divmod(n, 10)` extracts digits cleanly.
   Faster and more Pythonic than repeated `// 10` and `% 10`.
4. Early Exit: Return False the moment you detect a cycle (seen value).
   Don't wait for the sequence to "prove" it's infinite.
"""


class Solution:
    def is_happy(self, n: int) -> bool:
        """
        PROBLEM: HAPPY NUMBER
        Write an algorithm to determine if a number n is happy.

        A happy number is a number defined by the following process:
        - Starting with any positive integer, replace the number by the sum
          of the squares of its digits.
        - Repeat the process until the number equals 1 (where it will stay),
          or it loops endlessly in a cycle which does not include 1.
        - Those numbers for which this process ends in 1 are happy.

        Return True if n is a happy number, False otherwise.

        REQUIREMENTS:
        - Return True if the number is happy, False if it cycles.
        - Time Complexity must be O(log n) per iteration (digit extraction).
        - Space Complexity must be O(log n) for the seen set (bounded by cycle length).

        :param n: A positive integer.
        :return: True if n is happy, False otherwise.
        """
        if n < 0:
            return False

        # Space: O(c) where c is cycle length (bounded constant, typically < 20)
        # Time: O(log n) per iteration for digit extraction
        visited = set()
        while n != 1 and n not in visited:
            n_sum = 0
            # Time: O(log n) - extract each digit via string conversion
            for num in str(n):
                n_sum += int(num) ** 2
            visited.add(n)
            n = n_sum

        # Overall Time Complexity: O(log n) per iteration × bounded iterations = O(log n)
        # Overall Space Complexity: O(1) - cycle length bounded by constant
        return n == 1


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_happy_number_19(self):
        # 19 → 1² + 9² = 82 → 8² + 2² = 68 → 6² + 8² = 100 → 1² + 0² + 0² = 1
        self.assertTrue(self.sol.is_happy(19))

    def test_happy_number_1(self):
        # 1 is already happy
        self.assertTrue(self.sol.is_happy(1))

    def test_not_happy_number_2(self):
        # 2 → 4 → 16 → 37 → 58 → 89 → 145 → 42 → 20 → 4 (cycle)
        self.assertFalse(self.sol.is_happy(2))

    def test_not_happy_number_4(self):
        # 4 enters the same cycle as 2
        self.assertFalse(self.sol.is_happy(4))

    def test_happy_number_7(self):
        # 7 → 49 → 97 → 130 → 10 → 1
        self.assertTrue(self.sol.is_happy(7))

    def test_happy_number_10(self):
        # 10 → 1² + 0² = 1
        self.assertTrue(self.sol.is_happy(10))

    def test_not_happy_number_11(self):
        # 11 → 2 → cycle
        self.assertFalse(self.sol.is_happy(11))


if __name__ == "__main__":
    unittest.main()
