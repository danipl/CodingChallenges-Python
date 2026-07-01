import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: HASHING (EASY)
--------------------------------------------
1. collections.Counter(s): Builds a frequency map in O(n). Ideal for "how many of each
   character/word" problems — avoids manual dict bookkeeping.
2. dict.setdefault(key, default): Atomic "insert if missing, return existing" — cleaner
   than `if key not in d: d[key] = ...`.
3. zip(a, b): Pairs elements from two iterables positionally. Perfect for comparing
   two sequences in lockstep (e.g., pattern chars vs. words).
4. set() for "seen" tracking: O(1) membership test. Use when you need to ensure no
   two keys map to the same value (bijective / invertible mapping check).
5. str.split(): Splits on whitespace, drops empty strings. Returns list — pair with
   len() check to early-exit on length mismatch.
"""


class Solution:
    def wordPattern(self, pattern: str, s: str) -> bool:
        """
        PROBLEM: Word Pattern

        Given a pattern (lowercase letters) and a string s of space-separated words,
        determine whether s follows the same pattern.

        "Follows" means there is a full one-to-one (bijective) mapping between each
        character in pattern and each word in s:
          - Each character maps to exactly one word.
          - Each word maps to exactly one character.
          - No two characters map to the same word, and no two words map to the
            same character.

        EXAMPLES:
          pattern = "abba", s = "dog cat cat dog"   -> True
          pattern = "abba", s = "dog cat fish dog"  -> False  (a->dog and a->dog OK,
                                                          but b->cat and b->fish violates b's mapping)
          pattern = "aaaa", s = "dog cat cat dog"   -> False  (a can't map to 4 different words)
          pattern = "abba", s = "dog dog dog dog"   -> False  (a->dog and b->dog violates bijection)

        REQUIREMENTS:
          - Return True if s follows the pattern, False otherwise.
          - 1 <= pattern.length <= 300
          - 1 <= s.length <= 3000
          - s contains only lowercase letters and spaces.
          - Time Complexity must be O(n) where n = len(pattern).
          - Space Complexity must be O(n) for the mapping structures.

        :param pattern: String of lowercase letters representing the pattern.
        :param s: Space-separated string of words.
        :return: True if s follows the pattern, False otherwise.
        """
        if not s and not pattern:
            return True
        elif not s or not pattern:
            return False

        words = s.strip().split(" ")
        # Time: O(n) - split scans entire string once
        # Space: O(n) - words list stores all tokens
        if len(pattern) != len(words):
            return False

        relation = {}
        present = set()
        # Space: O(n) - dict + set store up to n mappings

        # Time: O(n) - single pass through pattern and words in lockstep
        for ch, word in zip(pattern, words):
            if ch in relation and relation[ch] != word:
                return False
            elif word in present and ch not in relation:
                return False
            relation[ch] = word
            present.add(word)

        # Overall Time Complexity: O(n) - single pass, all operations O(1) amortized
        # Overall Space Complexity: O(n) - dict + set store up to n entries
        return True


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_basic_match(self):
        self.assertTrue(self.sol.wordPattern("abba", "dog cat cat dog"))

    def test_broken_mapping(self):
        self.assertFalse(self.sol.wordPattern("abba", "dog cat fish dog"))

    def test_one_char_maps_to_many_words(self):
        self.assertFalse(self.sol.wordPattern("aaaa", "dog cat cat dog"))

    def test_two_chars_map_to_same_word(self):
        self.assertFalse(self.sol.wordPattern("abba", "dog dog dog dog"))

    def test_single_element(self):
        self.assertTrue(self.sol.wordPattern("a", "dog"))

    def test_length_mismatch(self):
        self.assertFalse(self.sol.wordPattern("abc", "dog cat"))

    def test_longer_pattern_than_words(self):
        self.assertFalse(self.sol.wordPattern("abba", "dog"))

    def test_all_same(self):
        self.assertTrue(self.sol.wordPattern("aaa", "dog dog dog"))


if __name__ == "__main__":
    unittest.main()
