import unittest

"""  
PYTHON INTERVIEW CHEAT-SHEET: SLIDING WINDOW (MEDIUM)  
------------------------------------------  
1. collections.Counter: Perfect for tracking character frequencies within 
   a window. It’s a subclass of dict with $O(1)$ average access.
2. set(): Use a set to track "seen" elements in $O(1)$ time if you only 
   need to check for existence/uniqueness.
3. max()/min(): These are highly optimized in Python. Use them to update 
   your global result instead of manual `if` checks to keep code clean.
4. Window Invariant: Always define what your window represents (e.g., 
   "all unique characters between left and right").
"""


class Solution:
    def length_of_longest_substring(self, s: str) -> int:
        """
        PROBLEM: LONGEST SUBSTRING WITHOUT REPEATING CHARACTERS
        Given a string `s`, find the length of the longest substring
        without repeating characters.

        REQUIREMENTS:
        - Return the integer length of the longest unique substring.
        - Time Complexity must be $O(n)$.
        - Space Complexity should be $O(min(n, m))$ where m is the alphabet size (character set).

        :param s: The input string.
        :return: The length of the longest substring.
        """
        result, slow_idx, = 0, 0
        # O(min(n, m)) space - stores at most min(n, m) character-index pairs where n is string length and m is alphabet size
        aux_set: dict[str, int] = dict()

        for fast_idx, val in enumerate(s):  # O(n) time, O(1) space - iterate through string once
            if val in aux_set:
                slow_idx = max(slow_idx + 1, aux_set[val] + 1)

            result = max(result, fast_idx + 1 - slow_idx)
            aux_set[val] = fast_idx

        return result


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_case(self):
        # "abc" is the longest substring
        self.assertEqual(self.sol.length_of_longest_substring("abcabcbb"), 3)

    def test_palindrome_case(self):
        # "ab" is the longest substring
        self.assertEqual(self.sol.length_of_longest_substring("abba"), 2)

    def test_all_same_chars(self):
        # "b" is the longest substring
        self.assertEqual(self.sol.length_of_longest_substring("bbbbb"), 1)

    def test_sliding_window_jump(self):
        # "wke" is the longest substring (note "pwke" is not a substring)
        self.assertEqual(self.sol.length_of_longest_substring("pwwkew"), 3)

    def test_empty_string(self):
        self.assertEqual(self.sol.length_of_longest_substring(""), 0)

    def test_single_char(self):
        self.assertEqual(self.sol.length_of_longest_substring(" "), 1)

    def test_all_unique(self):
        self.assertEqual(self.sol.length_of_longest_substring("au"), 2)


if __name__ == "__main__":
    unittest.main()
