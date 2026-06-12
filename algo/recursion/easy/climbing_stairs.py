import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: RECURSION (EASY - MEMOIZATION)
------------------------------------------
1. `@functools.lru_cache(maxsize=None)`: One-line memoization decorator.
   Caches every unique call signature automatically. Turns $O(2^n)$ recursion
   into $O(n)$ — the single most powerful interview trick for DP problems.
2. Base case first: Always define the termination condition at the top of your
   recursive function. Without it, you get `RecursionError: maximum recursion depth exceeded`.
3. `sys.setrecursionlimit(n)`: Python defaults to 1000 stack frames. For deep
   recursion, increase it: `import sys; sys.setrecursionlimit(2000)`.
4. Recursive relation: Identify how `f(n)` decomposes into smaller subproblems.
   Climbing stairs: `f(n) = f(n-1) + f(n-2)` — you arrive at step n from n-1 or n-2.
5. Manual memoization with dict: When `@lru_cache` isn't allowed, use
   `memo = {}; if n in memo: return memo[n]; memo[n] = result; return result`.
"""


class Solution:

    def __init__(self):
        self.memo = {}

    def climb_stairs(self, n: int) -> int:
        """
        PROBLEM: CLIMBING STAIRS
        You are climbing a staircase. It takes n steps to reach the top.
        Each time you can either climb 1 or 2 steps.

        Return the number of distinct ways to climb to the top.

        REQUIREMENTS:
        - Return the total number of distinct ways to reach step n.
        - You can take either 1 step or 2 steps at a time.
        - n >= 1 (at least 1 step).
        - Time Complexity must be O(n) — naive recursion O(2^n) is NOT acceptable.
        - Space Complexity must be O(n) for the recursion stack + memoization cache.

        :param n: The total number of steps to the top.
        :return: The number of distinct ways to climb to the top.

        Example 1:
            Input: n = 2
            Output: 2
            Explanation: Two ways: (1+1) or (2).

        Example 2:
            Input: n = 3
            Output: 3
            Explanation: Three ways: (1+1+1), (1+2), (2+1).

        Example 3:
            Input: n = 5
            Output: 8
            Explanation: Eight distinct combinations of 1-step and 2-step moves.
        """
        if n <= 2:
            self.memo[n] = n
            return max(0, n)
        elif n in self.memo:
            return self.memo[n]

        # Space: O(n) - memo dict stores up to n entries
        # Time: O(n) - each subproblem computed once due to memoization
        self.memo[n - 1] = self.climb_stairs(n - 1)
        self.memo[n - 2] = self.climb_stairs(n - 2)

        self.memo[n] = self.memo[n - 1] + self.memo[n - 2]

        # Overall Time Complexity: O(n) - each value from 3 to n computed exactly once
        # Overall Space Complexity: O(n) - recursion stack depth + memo dict stores n entries
        return self.memo[n]


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_one_step(self):
        """Only one way: take 1 step."""
        self.assertEqual(self.sol.climb_stairs(1), 1)

    def test_two_steps(self):
        """Two ways: (1+1) or (2)."""
        self.assertEqual(self.sol.climb_stairs(2), 2)

    def test_three_steps(self):
        """Three ways: (1+1+1), (1+2), (2+1)."""
        self.assertEqual(self.sol.climb_stairs(3), 3)

    def test_five_steps(self):
        """Eight ways — Fibonacci sequence: 1, 2, 3, 5, 8."""
        self.assertEqual(self.sol.climb_stairs(5), 8)

    def test_ten_steps(self):
        """Larger input to verify memoization handles it efficiently."""
        self.assertEqual(self.sol.climb_stairs(10), 89)

    def test_fifteen_steps(self):
        """Even larger — should still be instant with memoization."""
        self.assertEqual(self.sol.climb_stairs(15), 987)

    def test_single_step_edge(self):
        """Minimum valid input."""
        self.assertEqual(self.sol.climb_stairs(1), 1)


if __name__ == "__main__":
    unittest.main()
