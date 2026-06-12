import collections
import unittest
from typing import List

"""
PYTHON INTERVIEW CHEAT-SHEET: GRAPHS (MEDIUM - GRID TRAVERSAL / FLOOD FILL)
------------------------------------------
1. Grid as implicit graph: Each cell (r, c) is a node. Neighbors are
   (r+1, c), (r-1, c), (r, c+1), (r, c-1). No adjacency list needed —
   compute neighbors on the fly with bounds checking.
2. In-place visited marking: Instead of a separate `visited` set, mutate
   the grid: `grid[r][c] = '0'` after visiting. Saves O(m*n) extra space.
3. Directions array: `directions = [(0,1),(0,-1),(1,0),(-1,0)]` lets you
   loop over neighbors without repeating boundary checks four times.
4. DFS vs BFS on grids: DFS (recursive) is shorter to write and uses call
   stack space O(m*n) worst case. BFS (deque) uses O(min(m,n)) for the
   queue but more boilerplate. Both are $O(m \times n)$ time.
5. Boundary guard: `if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] == '0': return`
   — one-liner at the top of your DFS/BFS helper prevents all edge cases.

🆕 PATTERN TRANSFER: You've used BFS on trees (level_order_traversal.py) and
explicit graphs (keys_and_rooms.py, number_of_connected_components.py). Grid
traversal is the same reachability logic — but neighbors are computed from
coordinates, not stored in an adjacency list. In-place marking replaces the
`visited` set you used before.
"""


class Solution:
    def num_islands(self, grid: List[List[str]]) -> int:
        """
        PROBLEM: NUMBER OF ISLANDS

        Given an m x n 2D binary grid 'grid' where '1' represents land and
        '0' represents water, return the number of islands.

        An island is surrounded by water and is formed by connecting adjacent
        lands horizontally or vertically (4-directional connectivity). You may
        assume all four edges of the grid are surrounded by water.

        REQUIREMENTS:
        - Return the total number of distinct islands.
        - Two land cells belong to the same island if they are connected
          horizontally or vertically (NOT diagonally).
        - Grid dimensions: 1 <= m, n <= 300.
        - grid[r][c] is '0' or '1'.
        - Time Complexity must be O(m * n) — every cell visited at most once.
        - Space Complexity must be O(m * n) worst case (recursion stack / queue)
          or O(1) auxiliary if modifying the grid in-place is allowed.

        :param grid: A 2D list of '0's (water) and '1's (land).
        :return: The number of connected land components (islands).

        Example 1:
            Input: grid = [
                ["1","1","1","1","0"],
                ["1","1","0","1","0"],
                ["1","1","0","0","0"],
                ["0","0","0","0","0"]
            ]
            Output: 1
            Explanation: All '1's are connected — one island.

        Example 2:
            Input: grid = [
                ["1","1","0","0","0"],
                ["1","1","0","0","0"],
                ["0","0","1","0","0"],
                ["0","0","0","1","1"]
            ]
            Output: 3
            Explanation: Top-left 2x2 block, center cell, and bottom-right
            pair are three separate islands.

        Example 3:
            Input: grid = [["1"]]
            Output: 1
            Explanation: Single land cell — one island.

        Example 4:
            Input: grid = [["0"]]
            Output: 0
            Explanation: Single water cell — no islands.
        """
        if not grid:
            return 0

        islands = 0
        queue = collections.deque()

        # Space: O(1) auxiliary - in-place grid marking replaces visited set
        # Time: O(m * n) - outer loop visits each cell once, inner BFS visits each land cell and its 4 edges once
        for x in range(len(grid)):
            for y in range(len(grid[x])):
                if grid[x][y] == "0":
                    continue
                queue.append((x, y))
                grid[x][y] = "0"
                islands += 1
                while queue:
                    cx, cy = queue.popleft()
                    # Time: O(1) per neighbor - constant 4 directions checked
                    # Space: O(min(m, n)) - queue bounded by BFS frontier (smaller grid dimension)
                    if cx - 1 >= 0 and grid[cx - 1][cy] == "1":
                        grid[cx - 1][cy] = "0"
                        queue.append((cx - 1, cy))
                    if cx + 1 < len(grid) and grid[cx + 1][cy] == "1":
                        grid[cx + 1][cy] = "0"
                        queue.append((cx + 1, cy))
                    if cy - 1 >= 0 and grid[cx][cy - 1] == "1":
                        grid[cx][cy - 1] = "0"
                        queue.append((cx, cy - 1))
                    if cy + 1 < len(grid[cx]) and grid[cx][cy + 1] == "1":
                        grid[cx][cy + 1] = "0"
                        queue.append((cx, cy + 1))

        # Overall Time Complexity: O(m * n) - each cell scanned once, each land cell enqueued/dequeued once
        # Overall Space Complexity: O(min(m, n)) - queue bounded by BFS frontier; grid modified in-place
        return islands


class TestSolution(unittest.TestCase):
    def setUp(self):
        self.sol = Solution()

    def test_single_island(self):
        """All land cells connected — one island."""
        grid = [
            ["1", "1", "1", "1", "0"],
            ["1", "1", "0", "1", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "0", "0", "0"],
        ]
        self.assertEqual(self.sol.num_islands(grid), 1)

    def test_three_islands(self):
        """Three separate land components."""
        grid = [
            ["1", "1", "0", "0", "0"],
            ["1", "1", "0", "0", "0"],
            ["0", "0", "1", "0", "0"],
            ["0", "0", "0", "1", "1"],
        ]
        self.assertEqual(self.sol.num_islands(grid), 3)

    def test_single_land_cell(self):
        """Minimal grid with one land cell."""
        self.assertEqual(self.sol.num_islands([["1"]]), 1)

    def test_single_water_cell(self):
        """Minimal grid with no land."""
        self.assertEqual(self.sol.num_islands([["0"]]), 0)

    def test_all_water(self):
        """Entire grid is water — zero islands."""
        grid = [
            ["0", "0", "0"],
            ["0", "0", "0"],
            ["0", "0", "0"],
        ]
        self.assertEqual(self.sol.num_islands(grid), 0)

    def test_all_land(self):
        """Entire grid is land — one island."""
        grid = [
            ["1", "1", "1"],
            ["1", "1", "1"],
            ["1", "1", "1"],
        ]
        self.assertEqual(self.sol.num_islands(grid), 1)

    def test_diagonal_not_connected(self):
        """Diagonal '1's are NOT connected — two separate islands."""
        grid = [
            ["1", "0"],
            ["0", "1"],
        ]
        self.assertEqual(self.sol.num_islands(grid), 2)

    def test_single_row(self):
        """1-row grid with alternating land/water."""
        self.assertEqual(self.sol.num_islands([["1", "0", "1", "0", "1"]]), 3)

    def test_single_column(self):
        """1-column grid with separated land cells."""
        grid = [["1"], ["0"], ["1"], ["1"], ["0"], ["1"]]
        self.assertEqual(self.sol.num_islands(grid), 3)

    def test_snake_pattern(self):
        """Land cells form a winding path — still one island."""
        grid = [
            ["1", "1", "0", "0"],
            ["0", "1", "0", "0"],
            ["0", "1", "1", "1"],
            ["0", "0", "0", "1"],
        ]
        self.assertEqual(self.sol.num_islands(grid), 1)


if __name__ == "__main__":
    unittest.main()
