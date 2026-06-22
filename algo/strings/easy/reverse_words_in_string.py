import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: STRINGS (EASY - STRING REVERSAL)
---------------------------------------------------------------
1. str.split() (no args): Splits on any whitespace and removes empty strings.
   "  hello   world  ".split() → ["hello", "world"]. No manual filtering needed.
2. Slicing [::-1]: Reverses any sequence in O(n). Works on lists too:
   ["a", "b", "c"][::-1] → ["c", "b", "a"]. Use for word order reversal.
3. " ".join(list): Reconstructs string from list with single spaces.
   Always prefer join() over string concatenation in loops — O(n) vs O(n^2).
4. Two-pointer reversal (in-place): If asked to reverse without extra space,
   use two pointers swapping from ends toward center. O(1) space, O(n) time.
5. str.strip(): Removes leading/trailing whitespace. Use when input has
   extraneous spaces but you need clean boundaries.
"""


class Solution:
    def reverse_words(self, s: str) -> str:
        """
        PROBLEM: REVERSE WORDS IN A STRING
        Given an input string s, reverse the order of the words.

        A word is defined as a sequence of non-space characters. The words
        in s will be separated by at least one space.

        REQUIREMENTS:
        - Return a string of the words in reverse order, separated by single spaces.
        - The returned string should not contain leading or trailing spaces.
        - Multiple spaces between words should be reduced to a single space.
        - Time Complexity must be O(n).
        - Space Complexity must be O(n).

        :param s: The input string containing words separated by spaces.
        :return: String with words in reverse order.
        """
        if not s:
            return ""

        # Time: O(n) - split() scans string once, splits on whitespace
        # Space: O(n) - creates list of words
        # Time: O(n) - reversed() returns iterator, join() concatenates once
        # Space: O(n) - join() builds result string
        # Overall Time Complexity: O(n) - three linear passes (split, reverse, join)
        # Overall Space Complexity: O(n) - word list + result string
        return " ".join(reversed(s.split()))


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_basic_reversal(self):
        self.assertEqual(self.sol.reverse_words("the sky is blue"), "blue is sky the")

    def test_leading_trailing_spaces(self):
        self.assertEqual(self.sol.reverse_words("  hello world  "), "world hello")

    def test_multiple_spaces_between(self):
        self.assertEqual(self.sol.reverse_words("a good   example"), "example good a")

    def test_single_word(self):
        self.assertEqual(self.sol.reverse_words("hello"), "hello")

    def test_empty_string(self):
        self.assertEqual(self.sol.reverse_words(""), "")

    def test_only_spaces(self):
        self.assertEqual(self.sol.reverse_words("   "), "")

    def test_two_words(self):
        self.assertEqual(self.sol.reverse_words("hello world"), "world hello")

    def test_single_char_words(self):
        self.assertEqual(self.sol.reverse_words("a b c"), "c b a")


if __name__ == "__main__":
    unittest.main()
