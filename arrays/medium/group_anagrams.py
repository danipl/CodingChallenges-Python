import collections
import unittest

"""
PYTHON INTERVIEW CHEAT-SHEET: ARRAYS (MEDIUM - HASHING/STRINGS)
------------------------------------------
1. `collections.defaultdict(list)`: Eliminates the need for `if key not in dict` checks.
   Perfect for grouping items by a computed key.
2. `tuple(sorted(s))`: Strings are unhashable for dict keys, but tuples are not.
   Sorting a string and converting to tuple creates a canonical, hashable representation.
3. `ord(c) - ord('a')`: Convert characters to 0-25 indices for counting-sort-style
   frequency arrays. Faster than sorting for anagram detection: $O(n)$ vs $O(n \\log n)$.
4. `Counter(s) == Counter(t)`: Python's `collections.Counter` supports direct equality
   comparison—useful for quick anagram checks, though slower than canonical keys for grouping.
5. String immutability: Every string operation creates a new string. For heavy manipulation,
   consider `list` of chars and `''.join()` at the end.
"""


class Solution:
    def group_anagrams(self, strs: list[str]) -> list[list[str]]:
        """
        PROBLEM: GROUP ANAGRAMS
        Given an array of strings 'strs', group the anagrams together.
        Two strings are anagrams if they contain the exact same characters
        with the exact same frequencies.

        REQUIREMENTS:
        - Return a list of lists, where each inner list contains strings that are anagrams.
        - The order of groups and the order within groups does not matter.
        - All inputs consist of lowercase English letters only.
        - Time Complexity must be $O(n \\cdot k)$ or $O(n \\cdot k \\log k)$, where n is the
          number of strings and k is the maximum length of any string.
        - Space Complexity must be $O(n \\cdot k)$ to store the output.

        :param strs: A list of strings.
        :return: A list of lists of strings, grouped by anagram.
        """
        if not strs:
            return []

        # Space: O(n * k) - hash map stores all strings grouped by key
        # Time: O(n * k log k) - sort each string (max length k) to build canonical key
        anagrams = collections.defaultdict(list)

        for candidate in strs:
            # Time: O(k log k) - sort characters; Space: O(k) - tuple key
            anagrams[tuple(sorted(candidate))].append(candidate)

        # Overall Time Complexity: O(n * k log k) - n strings, each sorted in O(k log k)
        # Overall Space Complexity: O(n * k) - hash map stores all characters from all strings
        return list(anagrams.values())


class TestGroupAnagrams(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_standard_case(self):
        result = self.sol.group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        # Groups: [["eat","tea","ate"], ["tan","nat"], ["bat"]]
        expected = [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]
        self._assert_same_groups(result, expected)

    def test_empty_list(self):
        self.assertEqual(self.sol.group_anagrams([]), [])

    def test_single_element(self):
        result = self.sol.group_anagrams(["solo"])
        self.assertEqual(result, [["solo"]])

    def test_all_same_anagram(self):
        result = self.sol.group_anagrams(["abc", "bca", "cab", "acb"])
        expected = [["abc", "bca", "cab", "acb"]]
        self._assert_same_groups(result, expected)

    def test_no_anagrams(self):
        result = self.sol.group_anagrams(["abc", "def", "ghi"])
        expected = [["abc"], ["def"], ["ghi"]]
        self._assert_same_groups(result, expected)

    def test_empty_strings(self):
        result = self.sol.group_anagrams(["", "", "a", ""])
        expected = [["", "", ""], ["a"]]
        self._assert_same_groups(result, expected)

    def test_single_char_strings(self):
        result = self.sol.group_anagrams(["a", "b", "a", "c", "b"])
        expected = [["a", "a"], ["b", "b"], ["c"]]
        self._assert_same_groups(result, expected)

    def _assert_same_groups(self, result, expected):
        """Helper: compare groups regardless of order."""
        self.assertEqual(len(result), len(expected))
        result_sorted = sorted([sorted(g) for g in result])
        expected_sorted = sorted([sorted(g) for g in expected])
        self.assertEqual(result_sorted, expected_sorted)


if __name__ == "__main__":
    unittest.main()
