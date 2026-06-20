import collections
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: STRINGS (EASY - CHARACTER FREQUENCY)
-------------------------------------------------------------------
1. collections.Counter: One-liner for frequency counting. `Counter(s)` returns
   a dict-like object with character counts. O(n) time, O(k) space where k = unique chars.
2. Two-pass pattern: First pass builds frequency map, second pass finds the answer.
   Essential for "first occurrence" problems.
3. String iteration: `for i, char in enumerate(s):` gives both index and character.
   Use when you need the position, not just the character.
4. Return -1 convention: When a problem asks for an index and no valid answer exists,
   return -1. This is standard in Python/Java interviews.
5. ASCII vs Unicode: For lowercase English letters, you can use a fixed-size array
   of 26 elements instead of a hash map. But Counter is more Pythonic and general.
"""


class Solution:
    def first_uniq_char(self, s: str) -> int:
        """
        PROBLEM: FIRST UNIQUE CHARACTER IN A STRING
        Given a string s, find the first non-repeating character and return its index.
        If no such character exists, return -1.

        REQUIREMENTS:
        - Return the index of the first character that appears exactly once.
        - If no unique character exists, return -1.
        - Must solve in O(n) time complexity.
        - Handle empty strings gracefully.

        :param s: The input string (lowercase English letters).
        :return: Index of the first unique character, or -1 if none exists.

        Example 1:
            Input: s = "leetcode"
            Output: 0
            Explanation: 'l' appears once and is at index 0.

        Example 2:
            Input: s = "loveleetcode"
            Output: 2
            Explanation: 'v' appears once and is at index 2.

        Example 3:
            Input: s = "aabb"
            Output: -1
            Explanation: All characters repeat, no unique character.

        Example 4:
            Input: s = "abcabc"
            Output: -1
            Explanation: All characters appear twice.
        """
        if not s:
            return -1

        # Space: O(k) - hash map stores at most k unique characters (26 for lowercase English)
        chr_map = collections.defaultdict(lambda: 0)

        # Time: O(n) - iterate through string once to build frequency map
        for char in s:
            chr_map[char] += 1

        # Time: O(n) - iterate through string again to find first unique character
        for idx, char in enumerate(s):
            if chr_map[char] == 1:
                return idx

        # Overall Time Complexity: O(n) - two passes through the string
        # Overall Space Complexity: O(k) - hash map stores unique characters
        return -1


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_first_char_unique(self):
        """String: 'leetcode'. First unique is 'l' at index 0."""
        self.assertEqual(self.sol.first_uniq_char("leetcode"), 0)

    def test_middle_char_unique(self):
        """String: 'loveleetcode'. First unique is 'v' at index 2."""
        self.assertEqual(self.sol.first_uniq_char("loveleetcode"), 2)

    def test_no_unique_chars(self):
        """String: 'aabb'. All characters repeat."""
        self.assertEqual(self.sol.first_uniq_char("aabb"), -1)

    def test_all_same_chars(self):
        """String: 'aaaa'. No unique character."""
        self.assertEqual(self.sol.first_uniq_char("aaaa"), -1)

    def test_last_char_unique(self):
        """String: 'aabbccddz'. First unique is 'z' at index 8."""
        self.assertEqual(self.sol.first_uniq_char("aabbccddz"), 8)

    def test_single_char(self):
        """String: 'a'. Single character is unique."""
        self.assertEqual(self.sol.first_uniq_char("a"), 0)

    def test_empty_string(self):
        """Empty string — no unique character."""
        self.assertEqual(self.sol.first_uniq_char(""), -1)

    def test_two_chars_first_unique(self):
        """String: 'ab'. First unique is 'a' at index 0."""
        self.assertEqual(self.sol.first_uniq_char("ab"), 0)

    def test_two_chars_same(self):
        """String: 'aa'. No unique character."""
        self.assertEqual(self.sol.first_uniq_char("aa"), -1)

    def test_long_string(self):
        """String with unique char in middle."""
        s = "a" * 1000 + "z" + "b" * 1000
        self.assertEqual(self.sol.first_uniq_char(s), 1000)


if __name__ == "__main__":
    unittest.main()
