import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (EASY)
------------------------------------------
1. float('inf'): Use this to initialize a 'minimum' variable. It is 
   guaranteed to be larger than any numeric value in your data.
2. max() and min(): Instead of writing manual 'if' blocks, use these built-in 
   functions. They are concise and highly optimized in CPython.
3. Negative Indexing: `nums[-1]` is the fastest way to get the last element.
4. Range-based Loops: When you only need values and not indices, 
   `for price in prices:` is cleaner than `range(len(prices))`.
"""


class Solution:
    def max_profit(self, prices: list[int]) -> int:
        """
        PROBLEM: BEST TIME TO BUY AND SELL STOCK
        You are given an array 'prices' where prices[i] is the price of a
        given stock on the i-th day.

        You want to maximize your profit by choosing a single day to buy
        one stock and choosing a different day in the future to sell it.

        REQUIREMENTS:
        - Return the maximum profit you can achieve.
        - If you cannot achieve any profit, return 0.
        - Time Complexity must be O(n).
        - Space Complexity must be O(1).

        :param prices: A list of integers (stock prices).
        :return: The maximum integer profit.
        """
        if len(prices) < 2:  # Time: O(1) - constant time check, Space: O(1)
            return 0

        min_price = float('inf')  # Space: O(1) - single variable to track minimum price seen so far
        max_p = 0  # Space: O(1) - single variable to track maximum profit
        for price in prices:  # Time: O(n) - iterate through all prices once
            min_price = min(min_price, price)  # Time: O(1) - update minimum price if current is lower
            max_p = max(max_p, price - min_price)  # Time: O(1) - calculate profit and update maximum

        return max_p  # Time: O(1) - return result

class TestBestTimeToBuySell(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_case(self):
        # Buy on day 2 (price 1), sell on day 5 (price 6), profit = 5
        self.assertEqual(self.sol.max_profit([7, 1, 5, 3, 6, 4]), 5)

    def test_decreasing_prices(self):
        # No profit possible
        self.assertEqual(self.sol.max_profit([7, 6, 4, 3, 1]), 0)

    def test_single_day(self):
        # Cannot sell if you only have one day
        self.assertEqual(self.sol.max_profit([5]), 0)

    def test_valley_at_end(self):
        # Profit comes from earlier peak
        self.assertEqual(self.sol.max_profit([2, 4, 1]), 2)

    def test_volatile_market(self):
        self.assertEqual(self.sol.max_profit([3, 2, 6, 5, 0, 3]), 4)


if __name__ == "__main__":
    unittest.main()
