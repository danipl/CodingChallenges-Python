import collections
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: STRINGS (EASY - ANAGRAM DETECTION)
-----------------------------------------------------------------
1. collections.Counter: `Counter(s)` builds a frequency map in O(n).
   Two strings are anagrams iff `Counter(s) == Counter(t)`. One-liner, idiomatic.
2. Fixed-size array for ASCII: If inputs are lowercase a-z, use `int[26]`
   instead of a hash map. Increment for s, decrement for t — all zeros means anagram.
   O(1) space (26 slots), O(n) time. Faster than Counter in practice.
3. Early exit on length mismatch: `if len(s) != len(t): return False`.
   Anagrams must have the same length. Check this before any counting.
4. Single-pass counter trick: Instead of building two separate maps and comparing,
   build one map: increment for s chars, decrement for t chars. If any value != 0,
   not an anagrams. Saves one full pass and one map allocation.
5. ord() for index math: `ord(c) - ord('a')` maps 'a'-'z' to 0-25.
   Use this when converting characters to array indices.
"""


class Solution:
    def is_anagram(self, s: str, t: str) -> bool:
        """
        PROBLEM: VALID ANAGRAM
        Given two strings s and t, return True if t is an anagram of s,
        and False otherwise.

        An anagram is a word or phrase formed by rearranging the letters
        of a different word or phrase, typically using all the original
        letters exactly once.

        REQUIREMENTS:
        - Return True if t is an anagram of s, False otherwise.
        - Both strings contain only lowercase English letters.
        - Time Complexity must be O(n).
        - Space Complexity must be O(1) (fixed alphabet of 26 letters).

        :param s: The first string.
        :param t: The second string.
        :return: Boolean indicating if t is an anagram of s.
        """
        if (s is None or t is None) or (len(s) != len(t)):
            return False

        # Space: O(k) - at most k unique characters (26 for lowercase a-z)
        counters = collections.defaultdict(lambda: 0)

        # Time: O(n) - single pass through both strings simultaneously
        for pos in range(len(s)):
            counters[s[pos]] += 1
            counters[t[pos]] -= 1

        # Time: O(k) - iterate through counter values (max 26)
        for count in counters.values():
            if count != 0:
                return False

        # Overall Time Complexity: O(n) - one pass through strings + one pass through unique chars
        # Overall Space Complexity: O(k) - dictionary stores at most k unique characters
        return True


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_basic_anagram(self):
        self.assertTrue(self.sol.is_anagram("anagram", "nagaram"))

    def test_not_anagram(self):
        self.assertFalse(self.sol.is_anagram("rat", "car"))

    def test_different_lengths(self):
        self.assertFalse(self.sol.is_anagram("ab", "a"))

    def test_empty_strings(self):
        self.assertTrue(self.sol.is_anagram("", ""))

    def test_same_string(self):
        self.assertTrue(self.sol.is_anagram("hello", "hello"))

    def test_single_char_match(self):
        self.assertTrue(self.sol.is_anagram("a", "a"))

    def test_single_char_mismatch(self):
        self.assertFalse(self.sol.is_anagram("a", "b"))

    def test_repeated_chars(self):
        self.assertTrue(self.sol.is_anagram("aabb", "bbaa"))

    def test_same_length_different_freq(self):
        self.assertFalse(self.sol.is_anagram("aab", "abb"))


if __name__ == "__main__":
    unittest.main()
