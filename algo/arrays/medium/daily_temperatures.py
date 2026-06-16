import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (MEDIUM - MONOTONIC STACK)
------------------------------------------
1. Stack stores INDICES, not values: `stack.append(i)` lets you compute distances
   with `i - stack[-1]`. Values are accessed via `temperatures[stack[-1]]`.
2. While-loop pop pattern: `while stack and temperatures[i] > temperatures[stack[-1]]:`
   pops and resolves all smaller elements. This is the core monotonic stack idiom.
3. Decreasing stack (default): Stack maintains decreasing order. When you see a larger
   element, pop smaller ones. Use this for "next greater element" problems.
4. Increasing stack: Reverse the comparison (`<` instead of `>`). Use for "next smaller
   element" problems. Less common but appears in histogram/trapping water variants.
5. Amortized O(n) time: Each element is pushed once and popped at most once. Total
   operations = 2n, so time complexity is O(n) despite the nested while-loop.
"""


class Solution:
    def daily_temperatures(self, temperatures: list[int]) -> list[int]:
        """
        PROBLEM: DAILY TEMPERATURES
        Given an array of integers 'temperatures' representing daily temperatures,
        return an array 'answer' such that answer[i] is the number of days you
        have to wait after the i-th day to get a warmer temperature.

        If there is no future day for which this is possible, set answer[i] == 0.

        REQUIREMENTS:
        - Return a list of integers where each element represents days until warmer temperature.
        - If no warmer day exists, the answer is 0.
        - temperatures.length >= 1.
        - 30 <= temperatures[i] <= 100.
        - Time Complexity must be O(n) — single pass with amortized stack operations.
        - Space Complexity must be O(n) for the stack and result array.

        :param temperatures: List of daily temperatures.
        :return: List where answer[i] = days until warmer temperature after day i.

        Example 1:
            Input: temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
            Output: [1, 1, 4, 2, 1, 1, 0, 0]
            Explanation:
            - Day 0 (73): Next warmer is day 1 (74) → 1 day
            - Day 1 (74): Next warmer is day 2 (75) → 1 day
            - Day 2 (75): Next warmer is day 6 (76) → 4 days
            - Day 3 (71): Next warmer is day 5 (72) → 2 days
            - Day 4 (69): Next warmer is day 5 (72) → 1 day
            - Day 5 (72): Next warmer is day 6 (76) → 1 day
            - Day 6 (76): No warmer day → 0
            - Day 7 (73): No warmer day → 0

        Example 2:
            Input: temperatures = [30, 40, 50, 60]
            Output: [1, 1, 1, 0]
            Explanation: Each day is warmer than the previous, except the last.

        Example 3:
            Input: temperatures = [30, 60, 90]
            Output: [1, 1, 0]
            Explanation: Strictly increasing — each day waits 1 day, last day waits 0.

        Example 4:
            Input: temperatures = [90, 80, 70, 60]
            Output: [0, 0, 0, 0]
            Explanation: Strictly decreasing — no day is warmer than a previous day.
        """
        if not temperatures:
            return []

        stack = []
        # Space: O(n) - answer array stores n integers
        answer = [0] * len(temperatures)

        # Time: O(n) - iterate through all n elements once
        for idx, temp in enumerate(temperatures):
            while stack and temp > temperatures[stack[-1]]:
                idx_popped = stack.pop()
                answer[idx_popped] = idx - idx_popped
            stack.append(idx)

        # Overall Time Complexity: O(n) - single pass, each element pushed/popped at most once (amortized)
        # Overall Space Complexity: O(n) - answer array O(n) + stack O(n) worst case
        return answer


class TestDailyTemperatures(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_leetcode_example(self):
        """Classic mixed case from LeetCode."""
        temps = [73, 74, 75, 71, 69, 72, 76, 73]
        expected = [1, 1, 4, 2, 1, 1, 0, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_strictly_increasing(self):
        """Each day is warmer than the previous — all answers are 1 except last."""
        temps = [30, 40, 50, 60, 70]
        expected = [1, 1, 1, 1, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_strictly_decreasing(self):
        """No day is warmer than a previous day — all answers are 0."""
        temps = [90, 80, 70, 60, 50]
        expected = [0, 0, 0, 0, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_single_element(self):
        """Only one day — no future day exists."""
        temps = [50]
        expected = [0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_two_elements_warmer(self):
        """Two days, second is warmer."""
        temps = [30, 40]
        expected = [1, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_two_elements_colder(self):
        """Two days, second is colder."""
        temps = [40, 30]
        expected = [0, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_all_same_temperature(self):
        """All days have the same temperature — no warmer day exists."""
        temps = [70, 70, 70, 70]
        expected = [0, 0, 0, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_large_gap(self):
        """Warm day appears after many cold days."""
        temps = [30, 30, 30, 30, 30, 100]
        expected = [5, 4, 3, 2, 1, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_alternating_pattern(self):
        """Alternating high and low temperatures."""
        temps = [50, 60, 50, 60, 50, 60]
        expected = [1, 0, 1, 0, 1, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)

    def test_valley_then_peak(self):
        """Temperature drops then rises sharply."""
        temps = [80, 70, 60, 70, 80, 90]
        expected = [5, 3, 1, 1, 1, 0]
        self.assertEqual(self.sol.daily_temperatures(temps), expected)


if __name__ == "__main__":
    unittest.main()
