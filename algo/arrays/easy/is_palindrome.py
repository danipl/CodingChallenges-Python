import unittest

"""  
PYTHON INTERVIEW CHEAT-SHEET: STRINGS & ARRAYS (EASY)  
------------------------------------------  
1. string.isalnum(): Returns True if all characters in the string are 
   alphanumeric (letters or numbers). Essential for filtering noise.
2. Case Normalization: Use `s.lower()` or `s.casefold()` (more aggressive) 
   to handle case-insensitive comparisons efficiently.
3. Slicing Reversal: `s[::-1]` creates a reversed copy of a string/list. 
   Fast, but remember it takes $O(n)$ space.
4. Two-Pointer Pattern: Using `left` and `right` indices to converge 
   toward the center is the gold standard for $O(1)$ space complexity.
"""


class Solution:
    def is_palindrome(self, s: str) -> bool:
        """
        PROBLEM: VALID PALINDROME
        A phrase is a palindrome if, after converting all uppercase letters into
        lowercase letters and removing all non-alphanumeric characters, it
        reads the same forward and backward.

        REQUIREMENTS:
        - Return `True` if it's a palindrome, `False` otherwise.
        - Ignore spaces, punctuation, and casing.
        - Time Complexity must be $O(n)$.
        - Space Complexity should aim for $O(1)$ (in-place check).

        :param s: The input string.
        :return: Boolean indicating if the string is a valid palindrome.
        """
        left_idx, right_idx = 0, (len(s) - 1)

        while left_idx < right_idx:  # O(n) time overall - loop runs at most n/2 iterations
            left_char = s[left_idx]
            right_char = s[right_idx]
            if not left_char.isalnum():
                left_idx += 1
                continue
            if not right_char.isalnum():
                right_idx -= 1
                continue

            if left_char.lower() != right_char.lower():
                return False

            left_idx += 1
            right_idx -= 1

        return True


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_palindrome(self):
        # "amanaplanacanalpanama"
        self.assertTrue(self.sol.is_palindrome("A man, a plan, a canal: Panama"))

    def test_non_palindrome(self):
        self.assertFalse(self.sol.is_palindrome("race a car"))

    def test_empty_string(self):
        # An empty string reads the same forward and backward
        self.assertTrue(self.sol.is_palindrome(" "))

    def test_numeric_palindrome(self):
        self.assertTrue(self.sol.is_palindrome("No 'x' in Nixon"))

    def test_only_symbols(self):
        # After filtering, it's an empty string
        self.assertTrue(self.sol.is_palindrome(".,"))


if __name__ == "__main__":
    unittest.main()
