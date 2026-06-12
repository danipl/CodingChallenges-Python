import unittest

"""  
PYTHON INTERVIEW CHEAT-SHEET: STRINGS (EASY)  
------------------------------------------  
1. Slicing [::-1]: The most idiomatic way to reverse a string or check for palindromes in O(n) time.  
2. str.isalnum(): Essential for "Valid Palindrome" style questions to filter out non-alphanumeric characters.  
3. ''.join(list): Strings are immutable; if you need to perform many modifications, convert to a list first, 
   then join at the end to maintain O(n) complexity instead of O(n^2).  
4. casefold(): A more aggressive version of .lower() that is better for caseless matching across different languages.
"""


class Solution:
    def is_palindrome(self, s: str) -> bool:
        """
        PROBLEM: VALID PALINDROME
        A phrase is a palindrome if, after converting all uppercase letters into lowercase
        letters and removing all non-alphanumeric characters, it reads the same forward and backward.

        REQUIREMENTS:
        - Return True if s is a palindrome, False otherwise.
        - Ignore casing and non-alphanumeric characters (e.g., " ", "!", ",").
        - Time Complexity must be O(n).
        - Space Complexity must be O(n) or O(1) depending on the approach.

        :param s: The input string.
        :return: Boolean indicating if it's a valid palindrome.
        """
        length = len(s)

        left_p = 0
        right_p = (length - 1) - left_p
        while left_p < right_p:  # O(n) time: iterating through half the string
            left_char = s[left_p]
            right_char = s[right_p]
            if not left_char.isalnum():
                left_p += 1
                continue
            if not right_char.isalnum():
                right_p -= 1
                continue
            if left_char.lower() != right_char.lower():
                return False

            left_p += 1
            right_p -= 1

        # Time: O(n) - comparing characters from both ends
        # Space: O(1) - only using two pointers, no additional data structures
        return True


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_case_1(self):
        # Standard palindrome
        self.assertEqual(self.sol.is_palindrome("A man, a plan, a canal: Panama"), True)

    def test_case_2(self):
        # Non-palindrome
        self.assertEqual(self.sol.is_palindrome("race a car"), False)

    def test_case_3(self):
        # Empty string (technically a palindrome)
        self.assertEqual(self.sol.is_palindrome(" "), True)

    def test_case_4(self):
        # Only non-alphanumeric
        self.assertEqual(self.sol.is_palindrome(".,"), True)

    def test_case_5(self):
        # Numeric palindrome
        self.assertEqual(self.sol.is_palindrome("0P"), False)


if __name__ == "__main__":
    unittest.main()
