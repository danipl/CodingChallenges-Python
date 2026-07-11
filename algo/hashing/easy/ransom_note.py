import collections
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: HASHING (EASY)
------------------------------------------
1. collections.Counter: Builds a frequency map of elements in O(N) time.
   Example: `counts = collections.Counter(magazine)`
2. dict.get(key, default): Retrieves a key's value or returns a default if it doesn't exist.
   Example: `counts[char] = counts.get(char, 0) + 1`
3. collections.defaultdict(type): Automatically initializes missing keys with a default constructor.
   Example: `counts = collections.defaultdict(int)`
4. Set Operations: Perfect for uniqueness checking or O(1) membership testing.
   Example: `unique_chars = set(ransom_note)`
"""


class Solution:
    def can_construct(self, ransom_note: str, magazine: str) -> bool:
        """
        PROBLEM: RANSOM NOTE

        Given two strings ransom_note and magazine, return True if ransom_note 
        can be constructed from magazine and False otherwise.

        Each letter in magazine can only be used once in ransom_note.

        REQUIREMENTS:
        - Return True if ransom_note can be constructed, False otherwise.
        - Handle edge cases like empty strings.
        - Both strings contain only lowercase English letters.
        - Time Complexity: O(N + M) where N = len(ransom_note) and M = len(magazine).
        - Space Complexity: O(1) auxiliary space (since alphabet size is constant 26).

        :param ransom_note: The string representing the ransom note.
        :param magazine: The string representing the magazine.
        :return: True if ransom_note can be constructed from magazine, else False.
        """
        if not ransom_note:
            return True
        elif not magazine:
            return False
        elif len(ransom_note) > len(magazine):
            return False
        
        # Space: O(k) - frequency map storing at most k unique characters (max 26)
        # Time: O(m) - build character counts of magazine
        c_count = collections.Counter(magazine)

        # Time: O(n) - iterate through ransom note to verify character counts
        for char in ransom_note:
            if c_count[char] == 0:
                # Overall Time Complexity: O(m + n) - early exit after scanning parts of ransom note
                # Overall Space Complexity: O(k) - auxiliary dictionary storing characters
                return False
            c_count[char] -= 1

        # Overall Time Complexity: O(m + n) - full scan of magazine and ransom note
        # Overall Space Complexity: O(k) - frequency map storage where k <= 26
        return True


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_basic_false(self):
        self.assertFalse(self.sol.can_construct("a", "b"))

    def test_insufficient_chars(self):
        self.assertFalse(self.sol.can_construct("aa", "ab"))

    def test_basic_true(self):
        self.assertTrue(self.sol.can_construct("aa", "aab"))

    def test_empty_ransom_note(self):
        self.assertTrue(self.sol.can_construct("", "abc"))

    def test_empty_magazine_fails(self):
        self.assertFalse(self.sol.can_construct("a", ""))

    def test_both_empty(self):
        self.assertTrue(self.sol.can_construct("", ""))

    def test_exact_match(self):
        self.assertTrue(self.sol.can_construct("anagram", "nagaram"))


if __name__ == "__main__":
    unittest.main()
