import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: STRINGS (MEDIUM - STACK VALIDATION)
-----------------------------------------------------------------
1. Stack for Matching Pairs: Use a list as a stack (`append()` / `pop()`).
   When you see an opening bracket, push it. When you see a closing bracket,
   pop and check if it matches. This is O(n) time, O(n) space.
2. Hash Map for Bracket Pairs: `mapping = {')': '(', ']': '[', '}': '{'}`
   lets you check matches in O(1) instead of multiple if/elif branches.
3. Early Exit on Mismatch: If the stack is empty when you try to pop, or if
   the popped value doesn't match the closing bracket, return False immediately.
4. Final Check: After processing all characters, the stack must be empty.
   If not, there are unmatched opening brackets → return False.
5. String Iteration: `for char in s:` is the Pythonic way to iterate over
   characters. Avoid index-based loops unless you need the position.
"""


class Solution:
    open_ops = {'(', '[', '{'}
    close_inv_op = {
        ')': '(',
        ']': '[',
        '}': '{'
    }

    def isValid(self, s: str) -> bool:
        """
        PROBLEM: VALID PARENTHESES

        Given a string 's' containing just the characters '(', ')', '{', '}',
        '[' and ']', determine if the input string is valid.

        A string is valid if:
        1. Open brackets are closed by the same type of brackets.
        2. Open brackets are closed in the correct order.
        3. Every close bracket has a corresponding open bracket of the same type.

        REQUIREMENTS:
        - Return True if the string is valid, False otherwise.
        - s consists of parentheses only '()[]{}'.
        - 1 <= len(s) <= 10^4.
        - Time Complexity must be O(n) - single pass through the string.
        - Space Complexity must be O(n) - stack stores at most n characters.

        :param s: A string containing only bracket characters.
        :return: True if the brackets are properly nested and matched, False otherwise.

        Example 1:
            Input: s = "()"
            Output: True

        Example 2:
            Input: s = "()[]{}"
            Output: True

        Example 3:
            Input: s = "(]"
            Output: False
            Explanation: '(' is closed by ']' — mismatched types.

        Example 4:
            Input: s = "([])"
            Output: True
            Explanation: Properly nested — '[' opens and closes inside '('.
        """
        if not s:
            return True

        stack = []
        for char in s:
            if char in self.open_ops:
                stack.append(char)
            else:
                if not stack or stack.pop() != self.close_inv_op[char]:
                    return False

        return not stack


class TestValidParentheses(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_simple_valid(self):
        self.assertTrue(self.sol.isValid("()"))

    def test_multiple_valid(self):
        self.assertTrue(self.sol.isValid("()[]{}"))

    def test_mismatched_types(self):
        self.assertFalse(self.sol.isValid("(]"))

    def test_nested_valid(self):
        self.assertTrue(self.sol.isValid("([])"))

    def test_nested_invalid(self):
        self.assertFalse(self.sol.isValid("([)]"))

    def test_unclosed_bracket(self):
        self.assertFalse(self.sol.isValid("("))

    def test_extra_closing_bracket(self):
        self.assertFalse(self.sol.isValid(")"))

    def test_empty_string(self):
        # Edge case: empty string is technically valid (no unmatched brackets)
        self.assertTrue(self.sol.isValid(""))

    def test_complex_nested(self):
        self.assertTrue(self.sol.isValid("{[()()]}"))

    def test_single_pair(self):
        self.assertTrue(self.sol.isValid("{}"))


if __name__ == "__main__":
    unittest.main()
