import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY / GREEDY)
------------------------------------------------------
1. Greedy Logic: In problems where you can make multiple transactions, 
   look for "local" gains. If you can profit from one day to the next, 
   take it! The sum of all local gains equals the maximum possible profit.
2. zip(arr, arr[1:]): A Pythonic way to iterate through pairs of 
   consecutive elements. `for prev, curr in zip(prices, prices[1:]):`
3. Summing with Generators: `sum(max(0, b - a) for a, b in ...)` is a 
   highly efficient, memory-friendly way to calculate totals in Python.
4. Complexity Awareness: Always state that O(n) is the goal when you only 
   need to see each element once to make a decision.
"""


class Solution:
    def best_max_profit(self, prices: list[int]) -> int:
        """
        PROBLEM: BEST TIME TO BUY AND SELL STOCK II
        You are given an integer array 'prices' where prices[i] is the
        price of a given stock on the i-th day.

        On each day, you may decide to buy and/or sell the stock. You can
        only hold at most one share of the stock at any time. However,
        you can buy it then immediately sell it on the same day.

        REQUIREMENTS:
        - Find and return the maximum profit you can achieve.
        - Time Complexity: O(n)
        - Space Complexity: O(1)

        :param prices: A list of integers.
        :return: Total maximum profit.
        """
        # Time: O(1), Space: O(1)
        if len(prices) < 2:
            return 0

        # Space: O(1)
        max_profit = 0

        # Time: O(n) where n = len(prices), as we iterate once through the array
        # Space: O(1) as we only use constant extra space
        for idx in range(1, len(prices)):
            diff = prices[idx] - prices[idx - 1]
            if diff > 0:
                max_profit += diff

        # Overall Time Complexity: O(n), Space Complexity: O(1)
        return max_profit


class TestBestTimeToBuySellTwo(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_multiple_gains(self):
        # Buy day 2 (1), sell day 3 (5). Profit = 4.
        # Buy day 4 (3), sell day 5 (6). Profit = 3. Total = 7.
        self.assertEqual(self.sol.best_max_profit([7, 1, 5, 3, 6, 4]), 7)

    def test_continuous_climb(self):
        # Buy day 1, sell day 5. Total profit = 4.
        # (Or buy/sell daily: 1->2, 2->3, 3->4, 4->5 = 1+1+1+1 = 4)
        self.assertEqual(self.sol.best_max_profit([1, 2, 3, 4, 5]), 4)

    def test_all_decreasing(self):
        self.assertEqual(self.sol.best_max_profit([7, 6, 4, 3, 1]), 0)

    def test_valley_and_peaks(self):
        self.assertEqual(self.sol.best_max_profit([2, 1, 4, 5, 2, 9, 7]), 11)

    def test_empty_or_single(self):
        self.assertEqual(self.sol.best_max_profit([]), 0)
        self.assertEqual(self.sol.best_max_profit([5]), 0)


if __name__ == "__main__":
    unittest.main()
